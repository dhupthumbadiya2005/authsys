// Simple WebAuthn test utility
export async function testWebAuthnSupport() {
  console.log('🧪 Testing WebAuthn Support...');
  
  // Check basic support
  if (!window.PublicKeyCredential) {
    console.error('❌ WebAuthn not supported');
    return false;
  }
  
  console.log('✅ WebAuthn API available');
  
  // Check if platform authenticator is available
  try {
    const available = await PublicKeyCredential.isUserVerifyingPlatformAuthenticatorAvailable();
    console.log('✅ Platform authenticator available:', available);
  } catch (e) {
    console.error('❌ Error checking platform authenticator:', e);
  }
  
  // Test simple credential creation
  try {
    console.log('🔧 Testing simple credential creation...');
    
    const challenge = new Uint8Array(32);
    crypto.getRandomValues(challenge);
    
    const userId = new Uint8Array(16);
    crypto.getRandomValues(userId);
    
    const createOptions = {
      challenge,
      rp: {
        name: "Test App",
        id: "localhost"
      },
      user: {
        id: userId,
        name: "testuser",
        displayName: "Test User"
      },
      pubKeyCredParams: [
        { alg: -7, type: "public-key" },  // ES256
        { alg: -257, type: "public-key" } // RS256
      ],
      timeout: 60000,
      authenticatorSelection: {
        userVerification: "preferred",
        requireResidentKey: false
      }
    };
    
    console.log('📋 Create options:', createOptions);
    
    // This should trigger the biometric prompt
    const credential = await navigator.credentials.create({
      publicKey: createOptions
    });
    
    console.log('🎉 Test credential created successfully!', credential);
    return true;
    
  } catch (error) {
    console.error('❌ Test credential creation failed:', error);
    console.error('Error name:', error.name);
    console.error('Error message:', error.message);
    return false;
  }
}

// Call this in browser console: testWebAuthnSupport()
window.testWebAuthnSupport = testWebAuthnSupport;
