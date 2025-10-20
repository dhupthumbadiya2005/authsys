import base64
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from ..models import (
    RegistrationBeginRequest, RegistrationCompleteRequest,
    LoginBeginRequest, LoginCompleteRequest, User, Credential, Challenge
)
from ..database import (
    get_user_by_username, create_user, get_credentials_by_user_id,
    create_credential, create_challenge, get_challenge, update_user_last_login,
    update_credential_sign_count
)
from ..utils.webauthn_utils import (
    generate_user_id, generate_challenge, create_registration_options,
    verify_registration, create_authentication_options, verify_authentication
)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.options("/{path:path}")
async def options_handler():
    """Handle OPTIONS requests for CORS preflight"""
    return {"message": "OK"}

@router.post("/register/begin")
async def register_begin(request: RegistrationBeginRequest):
    """Begin WebAuthn registration process"""
    try:
        # Check if user already exists
        existing_user = await get_user_by_username(request.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Generate user ID
        user_id = generate_user_id()
        
        # Create registration options
        options = await create_registration_options(request.username, user_id)
        
        # Use the challenge directly from options (it's already base64url encoded)
        challenge_b64url = base64.urlsafe_b64encode(options.challenge).decode().rstrip('=')
        
        
        # Store challenge in database
        challenge_data = Challenge(
            challenge=challenge_b64url,
            username=request.username,
            type="registration"
        ).model_dump(by_alias=True)
        
        await create_challenge(challenge_data)
        
        # Convert options to JSON-serializable format
        options_dict = {
            "rp": {"id": options.rp.id, "name": options.rp.name},
            "user": {
                "id": base64.urlsafe_b64encode(options.user.id).decode().rstrip('='),
                "name": options.user.name,
                "displayName": options.user.display_name
            },
            "challenge": challenge_b64url,
            "pubKeyCredParams": [{"alg": alg.alg, "type": "public-key"} for alg in options.pub_key_cred_params],
            "timeout": options.timeout,
            "authenticatorSelection": {
                "userVerification": options.authenticator_selection.user_verification.value if hasattr(options.authenticator_selection.user_verification, 'value') else str(options.authenticator_selection.user_verification).lower(),
                "requireResidentKey": False,
                "residentKey": "preferred"
            }
        }
        
        return {"options": options_dict, "user_id": user_id}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/register/complete")
async def register_complete(request: RegistrationCompleteRequest):
    """Complete WebAuthn registration process"""
    try:
        # Get client data JSON from credential response
        client_data_json_b64 = request.credential.get("response", {}).get("clientDataJSON", "")
        if not client_data_json_b64:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid credential response"
            )
        
        # Decode client data to get challenge
        import json
        client_data_json = base64.urlsafe_b64decode(
            client_data_json_b64 + "=" * (4 - len(client_data_json_b64) % 4)
        ).decode('utf-8')
        client_data = json.loads(client_data_json)
        received_challenge = client_data.get("challenge", "")
        
        # Debug logging
        print(f"DEBUG: Received challenge from client: {received_challenge}")
        print(f"DEBUG: Challenge length: {len(received_challenge)}")
        
        # Find any stored challenge for this user (we'll let WebAuthn library verify the challenge)
        from ..database import get_database
        database = await get_database()
        stored_challenge = await database.challenges.find_one_and_delete(
            {
                "username": request.username,
                "type": "registration",
                "expires_at": {"$gt": datetime.utcnow()}
            },
            sort=[("created_at", -1)]  # Get the most recent challenge
        )
        
        print(f"DEBUG: Stored challenge found: {stored_challenge is not None}")
        if stored_challenge:
            print(f"DEBUG: Stored challenge value: {stored_challenge.get('challenge', 'N/A')}")
        
        if not stored_challenge:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired challenge"
            )
        
        # Use the stored challenge for verification (let WebAuthn library handle the comparison)
        try:
            print(f"DEBUG: Starting WebAuthn verification...")
            print(f"DEBUG: Credential type: {type(request.credential)}")
            print(f"DEBUG: Credential keys: {list(request.credential.keys()) if isinstance(request.credential, dict) else 'Not a dict'}")
            
            verification = await verify_registration(request.credential, stored_challenge["challenge"], request.username)
            print(f"DEBUG: Verification result: {verification}")
            print(f"DEBUG: Verification successful - credential_id: {verification.credential_id}")
            
        except Exception as verify_error:
            print(f"DEBUG: WebAuthn verification failed with error: {verify_error}")
            print(f"DEBUG: Error type: {type(verify_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"WebAuthn verification error: {str(verify_error)}"
            )
        
        # If we get here, verification was successful (no exception thrown)
        print(f"DEBUG: Registration verification successful!")
        
        # Generate user ID for this registration
        user_id = generate_user_id()
        
        # Create user record
        user_data = User(
            username=request.username,
            user_id=user_id,
            display_name=request.username
        ).model_dump(by_alias=True)
        
        await create_user(user_data)
        
        # Store credential
        credential_data = Credential(
            user_id=user_id,
            credential_id=base64.urlsafe_b64encode(verification.credential_id).decode().rstrip('='),
            public_key=base64.urlsafe_b64encode(verification.credential_public_key).decode().rstrip('='),
            sign_count=verification.sign_count
        ).model_dump(by_alias=True)
        
        await create_credential(credential_data)
        
        return {"success": True, "message": "Registration completed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration completion failed: {str(e)}"
        )

@router.post("/login/begin")
async def login_begin(request: LoginBeginRequest):
    """Begin WebAuthn authentication process"""
    try:
        # Check if user exists
        user = await get_user_by_username(request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Get user's credentials
        credentials = await get_credentials_by_user_id(user["user_id"])
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No credentials found for user"
            )
        
        # Create authentication options
        options = await create_authentication_options(credentials)
        
        # Extract challenge from the generated options (like we do in registration)
        challenge_b64url = base64.urlsafe_b64encode(options.challenge).decode().rstrip('=')
        
        # Debug logging for login
        print(f"DEBUG LOGIN BEGIN: Generated challenge from options: {challenge_b64url}")
        print(f"DEBUG LOGIN BEGIN: Challenge length: {len(challenge_b64url)}")
        print(f"DEBUG LOGIN BEGIN: Raw challenge bytes length: {len(options.challenge)}")
        
        # Store challenge in database
        challenge_data = Challenge(
            challenge=challenge_b64url,
            username=request.username,
            type="authentication"
        ).model_dump(by_alias=True)
        
        await create_challenge(challenge_data)
        print(f"DEBUG LOGIN BEGIN: Stored challenge in DB: {challenge_b64url}")
        
        # Convert options to dict
        options_dict = {
            "challenge": challenge_b64url,
            "timeout": options.timeout,
            "rpId": options.rp_id,
            "allowCredentials": [
                {
                    "id": base64.urlsafe_b64encode(cred.id).decode().rstrip('='),
                    "type": "public-key",
                    "transports": [t for t in cred.transports]
                }
                for cred in options.allow_credentials
            ],
            "userVerification": options.user_verification
        }
        
        return {"options": options_dict}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login initiation failed: {str(e)}"
        )

@router.post("/login/complete")
async def login_complete(request: LoginCompleteRequest):
    """Complete WebAuthn authentication process"""
    try:
        # Find any stored challenge for this user (we'll let WebAuthn library verify the challenge)
        from ..database import get_database
        database = await get_database()
        
        # First, let's see all challenges for this user
        all_challenges = await database.challenges.find({
            "username": request.username,
            "type": "authentication"
        }).to_list(length=None)
        print(f"DEBUG LOGIN: All auth challenges for user: {all_challenges}")
        
        stored_challenge = await database.challenges.find_one_and_delete(
            {
                "username": request.username,
                "type": "authentication",
                "expires_at": {"$gt": datetime.utcnow()}
            },
            sort=[("created_at", -1)]  # Get the most recent challenge
        )
        
        print(f"DEBUG LOGIN: Retrieved stored challenge: {stored_challenge}")
        
        if not stored_challenge:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired challenge"
            )
        
        # Get user and credentials
        user = await get_user_by_username(request.username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        credentials = await get_credentials_by_user_id(user["user_id"])
        
        # Find matching credential
        credential_id = request.credential.get("id", "")
        stored_credential = None
        
        for cred in credentials:
            if cred["credential_id"] == credential_id:
                stored_credential = cred
                break
        
        if not stored_credential:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Credential not found"
            )
        
        # Verify authentication response
        try:
            print(f"DEBUG LOGIN: Starting WebAuthn authentication verification...")
            print(f"DEBUG LOGIN: Stored challenge: {stored_challenge['challenge']}")
            print(f"DEBUG LOGIN: Credential type: {type(request.credential)}")
            print(f"DEBUG LOGIN: Credential keys: {list(request.credential.keys()) if isinstance(request.credential, dict) else 'Not a dict'}")
            
            verification = await verify_authentication(
                request.credential, 
                stored_challenge["challenge"], 
                stored_credential
            )
            
            print(f"DEBUG LOGIN: Verification result: {verification}")
            print(f"DEBUG LOGIN: Verification successful!")
            
        except Exception as verify_error:
            print(f"DEBUG LOGIN: WebAuthn authentication verification failed with error: {verify_error}")
            print(f"DEBUG LOGIN: Error type: {type(verify_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"WebAuthn authentication verification error: {str(verify_error)}"
            )
        
        # If we get here, verification was successful (no exception thrown)
        
        # Update sign count (newer webauthn library uses new_sign_count)
        sign_count = getattr(verification, 'new_sign_count', getattr(verification, 'sign_count', 0))
        await update_credential_sign_count(credential_id, sign_count)
        
        # Update last login
        await update_user_last_login(request.username)
        
        return {
            "message": "Login successful",
            "username": request.username
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Authentication completion failed: {str(e)}"
        )
