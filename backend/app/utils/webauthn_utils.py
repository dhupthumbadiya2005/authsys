import os
import secrets
import base64
from webauthn import generate_registration_options, verify_registration_response
from webauthn import generate_authentication_options, verify_authentication_response
from webauthn.helpers.structs import (
    AuthenticatorSelectionCriteria,
    UserVerificationRequirement,
    PublicKeyCredentialDescriptor,
    AuthenticatorTransport
)
from webauthn.helpers.cose import COSEAlgorithmIdentifier

def generate_user_id() -> str:
    """Generate a random user ID for WebAuthn"""
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

def generate_challenge() -> str:
    """Generate a random challenge"""
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')

def get_rp_id() -> str:
    """Get Relying Party ID from environment"""
    return os.getenv("RP_ID", "localhost")

def get_rp_name() -> str:
    """Get Relying Party name from environment"""
    return os.getenv("RP_NAME", "AuthSys WebAuthn Demo")

def get_expected_origin():
    """Get expected origin based on RP_ID"""
    rp_id = get_rp_id()
    
    # For localhost, use http with port 5173
    if rp_id == "localhost":
        return "http://localhost:5173"
    
    # For IP addresses, use http with port 5173
    import re
    if re.match(r'^\d+\.\d+\.\d+\.\d+$', rp_id):
        return f"http://{rp_id}:5173"
    
    # For domain names, use https (no port for production)
    return f"https://{rp_id}"

async def create_registration_options(username: str, user_id: str):
    """Create WebAuthn registration options"""
    
    options = generate_registration_options(
        rp_id=get_rp_id(),
        rp_name=get_rp_name(),
        user_id=user_id.encode('utf-8'),
        user_name=username,
        user_display_name=username,
        authenticator_selection=AuthenticatorSelectionCriteria(
            user_verification=UserVerificationRequirement.PREFERRED,
            require_resident_key=False,
            resident_key="preferred"
        ),
        supported_pub_key_algs=[
            COSEAlgorithmIdentifier.ECDSA_SHA_256,
            COSEAlgorithmIdentifier.RSASSA_PKCS1_v1_5_SHA_256,
        ],
        timeout=60000,  # 60 seconds
    )
    
    return options

async def verify_registration(credential, challenge: str, username: str):
    """Verify WebAuthn registration response"""
    
    # Convert base64url challenge back to bytes
    challenge_bytes = base64.urlsafe_b64decode(challenge + "=" * (4 - len(challenge) % 4))
    
    verification = verify_registration_response(
        credential=credential,
        expected_challenge=challenge_bytes,
        expected_origin=get_expected_origin(),
        expected_rp_id=get_rp_id(),
    )
    
    return verification

async def create_authentication_options(credentials: list):
    """Create WebAuthn authentication options"""
    
    # Convert stored credentials to PublicKeyCredentialDescriptor format
    allow_credentials = []
    for cred in credentials:
        # Decode base64url credential ID
        credential_id_bytes = base64.urlsafe_b64decode(
            cred["credential_id"] + "=" * (4 - len(cred["credential_id"]) % 4)
        )
        
        allow_credentials.append(
            PublicKeyCredentialDescriptor(
                id=credential_id_bytes,
                transports=[
                    AuthenticatorTransport.USB,
                    AuthenticatorTransport.NFC,
                    AuthenticatorTransport.BLE,
                    AuthenticatorTransport.INTERNAL,
                ]
            )
        )
    
    options = generate_authentication_options(
        rp_id=get_rp_id(),
        allow_credentials=allow_credentials,
        user_verification=UserVerificationRequirement.PREFERRED,
    )
    
    return options

async def verify_authentication(credential, challenge: str, stored_credential: dict):
    """Verify WebAuthn authentication response"""
    
    # Convert base64url challenge back to bytes
    challenge_bytes = base64.urlsafe_b64decode(challenge + "=" * (4 - len(challenge) % 4))
    
    # Decode stored public key
    public_key_bytes = base64.urlsafe_b64decode(
        stored_credential["public_key"] + "=" * (4 - len(stored_credential["public_key"]) % 4)
    )
    
    # Decode credential ID
    credential_id_bytes = base64.urlsafe_b64decode(
        stored_credential["credential_id"] + "=" * (4 - len(stored_credential["credential_id"]) % 4)
    )
    
    verification = verify_authentication_response(
        credential=credential,
        expected_challenge=challenge_bytes,
        expected_origin=get_expected_origin(),
        expected_rp_id=get_rp_id(),
        credential_public_key=public_key_bytes,
        credential_current_sign_count=stored_credential["sign_count"],
    )
    
    return verification
