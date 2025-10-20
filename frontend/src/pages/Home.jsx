import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div style={{ padding: '40px 20px', textAlign: 'center', maxWidth: '800px', margin: '0 auto' }}>
      {/* Hero Section */}
      <div style={{ marginBottom: '40px' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '20px' }}>
          Welcome to AuthSys
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#666', marginBottom: '30px' }}>
          Experience passwordless biometric authentication. Secure, fast, and convenient - no passwords required.
        </p>
        
        <div style={{ display: 'flex', gap: '15px', justifyContent: 'center', flexWrap: 'wrap' }}>
          <Link
            to="/register"
            style={{
              display: 'inline-block',
              padding: '12px 24px',
              backgroundColor: '#007bff',
              color: 'white',
              textDecoration: 'none',
              borderRadius: '6px',
              fontWeight: 'bold'
            }}
          >
            Get Started
          </Link>
          <Link
            to="/login"
            style={{
              display: 'inline-block',
              padding: '12px 24px',
              backgroundColor: 'white',
              color: '#007bff',
              textDecoration: 'none',
              borderRadius: '6px',
              border: '2px solid #007bff',
              fontWeight: 'bold'
            }}
          >
            Sign In
          </Link>
        </div>
      </div>

      {/* Features */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: '20px', 
        marginBottom: '40px' 
      }}>
        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px',
          backgroundColor: '#f9f9f9'
        }}>
          <h3 style={{ marginBottom: '10px' }}>🔒 Passwordless</h3>
          <p>No passwords to remember, type, or worry about being stolen.</p>
        </div>

        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px',
          backgroundColor: '#f9f9f9'
        }}>
          <h3 style={{ marginBottom: '10px' }}>👆 Biometric Auth</h3>
          <p>Use your fingerprint, Face ID, or other biometric methods.</p>
        </div>

        <div style={{ 
          border: '1px solid #ddd', 
          borderRadius: '8px', 
          padding: '20px',
          backgroundColor: '#f9f9f9'
        }}>
          <h3 style={{ marginBottom: '10px' }}>🛡️ Secure</h3>
          <p>Built on WebAuthn standard with military-grade encryption.</p>
        </div>
      </div>

      {/* How it Works */}
      <div style={{ 
        border: '1px solid #ddd', 
        borderRadius: '8px', 
        padding: '30px',
        backgroundColor: 'white'
      }}>
        <h2 style={{ marginBottom: '30px' }}>How It Works</h2>
        <div style={{ 
          display: 'grid', 
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
          gap: '20px' 
        }}>
          <div>
            <div style={{ 
              width: '40px', 
              height: '40px', 
              backgroundColor: '#007bff', 
              color: 'white', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              margin: '0 auto 15px',
              fontWeight: 'bold'
            }}>
              1
            </div>
            <h3 style={{ marginBottom: '10px' }}>Register</h3>
            <p>Create your account and set up biometric authentication in seconds.</p>
          </div>
          
          <div>
            <div style={{ 
              width: '40px', 
              height: '40px', 
              backgroundColor: '#28a745', 
              color: 'white', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              margin: '0 auto 15px',
              fontWeight: 'bold'
            }}>
              2
            </div>
            <h3 style={{ marginBottom: '10px' }}>Authenticate</h3>
            <p>Use your fingerprint or Face ID to securely sign in.</p>
          </div>
          
          <div>
            <div style={{ 
              width: '40px', 
              height: '40px', 
              backgroundColor: '#dc3545', 
              color: 'white', 
              borderRadius: '50%', 
              display: 'flex', 
              alignItems: 'center', 
              justifyContent: 'center', 
              margin: '0 auto 15px',
              fontWeight: 'bold'
            }}>
              3
            </div>
            <h3 style={{ marginBottom: '10px' }}>Access</h3>
            <p>Enjoy secure access to your account without any passwords.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
