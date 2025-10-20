import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { authAPI } from '../utils/api';
import { registerWithWebAuthn } from '../utils/webauthn';

const Register = () => {
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    
    if (!username.trim()) {
      setError('Please enter a username');
      return;
    }

    setLoading(true);
    setError('');

    try {
      // Step 1: Begin registration
      const beginResponse = await authAPI.registerBegin(username);
      const { options } = beginResponse.data;

      // Step 2: Create credential with WebAuthn
      const credential = await registerWithWebAuthn(options);

      // Step 3: Complete registration
      await authAPI.registerComplete(username, credential);
      
      // Redirect to login page
      navigate('/login', { 
        state: { 
          message: 'Registration successful! Please sign in with your biometrics.' 
        }
      });

    } catch (err) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else if (err.message) {
        setError(err.message);
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '400px', margin: '50px auto' }}>
      <h2>Register</h2>
      <p>Create account with biometric authentication</p>
      
      <form onSubmit={handleRegister} style={{ marginTop: '20px' }}>
        <div style={{ marginBottom: '15px' }}>
          <label>Username or Email:</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{ 
              width: '100%', 
              padding: '8px', 
              marginTop: '5px',
              border: '1px solid #ccc',
              borderRadius: '4px'
            }}
            placeholder="Enter your username or email"
            disabled={loading}
            required
          />
        </div>

        {error && (
          <div style={{ 
            color: 'red', 
            backgroundColor: '#ffebee', 
            padding: '10px', 
            marginBottom: '15px',
            border: '1px solid #ffcdd2',
            borderRadius: '4px'
          }}>
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '10px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Registering...' : 'Register with Biometrics'}
        </button>
      </form>

      <p style={{ textAlign: 'center', marginTop: '20px' }}>
        Already have an account? <Link to="/login">Sign in here</Link>
      </p>
    </div>
  );
};

export default Register;
