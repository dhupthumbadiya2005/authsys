import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard = () => {
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const username = localStorage.getItem('currentUser');
    if (!username) {
      navigate('/login');
      return;
    }
    
    setCurrentUser(username);
    setLoading(false);
  }, [navigate]);

  const handleLogout = () => {
    localStorage.removeItem('currentUser');
    navigate('/login');
  };

  if (loading) {
    return (
      <div style={{ padding: '50px', textAlign: 'center' }}>
        <p>Loading...</p>
      </div>
    );
  }


  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ 
        border: '1px solid #ddd', 
        borderRadius: '8px', 
        padding: '20px', 
        marginBottom: '20px',
        backgroundColor: '#f9f9f9'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1>Dashboard</h1>
            <p>Welcome back, {currentUser}!</p>
          </div>
          <button
            onClick={handleLogout}
            style={{
              padding: '8px 16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Logout
          </button>
        </div>
      </div>

      {/* User Info */}
      <div style={{ 
        border: '1px solid #ddd', 
        borderRadius: '8px', 
        padding: '20px', 
        marginBottom: '20px'
      }}>
        <h2>Authentication Status</h2>
        <div style={{ marginTop: '15px' }}>
          <div style={{ marginBottom: '10px' }}>
            <strong>Authenticated User:</strong> {currentUser}
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Authentication Method:</strong> WebAuthn Biometric
          </div>
          <div style={{ marginBottom: '10px' }}>
            <strong>Session:</strong> Active
          </div>
        </div>
      </div>

      {/* Security Info */}
      <div style={{ 
        border: '1px solid #ddd', 
        borderRadius: '8px', 
        padding: '20px',
        backgroundColor: '#e8f5e8'
      }}>
        <h2>Security</h2>
        <div style={{ marginTop: '15px' }}>
          <p><strong>✓ WebAuthn Biometric Authentication</strong></p>
          <p>Your account is secured with passwordless biometric authentication</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
