# AuthSys - WebAuthn Passwordless Authentication System

A complete, production-ready passwordless authentication system using WebAuthn biometrics, built with FastAPI and React.

![WebAuthn](https://img.shields.io/badge/WebAuthn-Enabled-green)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-blue)
![React](https://img.shields.io/badge/React-18+-61DAFB)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green)

## 🚀 Features

### 🔐 Security
- **Passwordless Authentication** - No passwords to remember or steal
- **Biometric Login** - Touch ID, Face ID, Windows Hello, YubiKey support
- **WebAuthn Standard** - Industry-standard FIDO2/WebAuthn protocol
- **JWT Sessions** - Secure token-based session management
- **Challenge-Response** - Cryptographic challenge verification
- **Origin Validation** - Prevents phishing attacks

### 💻 User Experience
- **One-Click Registration** - Register with just biometrics
- **Instant Login** - Login in seconds with biometrics
- **Cross-Platform** - Works on desktop and mobile
- **Modern UI** - Clean, responsive React interface
- **Real-time Feedback** - Clear success/error messages

### 🛠 Technical Features
- **RESTful API** - Clean, documented FastAPI backend
- **MongoDB Integration** - Scalable NoSQL database
- **Real-time Validation** - Instant form validation
- **Error Handling** - Comprehensive error management
- **CORS Support** - Cross-origin resource sharing
- **Auto-cleanup** - TTL indexes for expired challenges

## 🏗 Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │   MongoDB Atlas  │
│                 │    │                 │    │                 │
│ • Registration  │◄──►│ • WebAuthn APIs │◄──►│ • Users         │
│ • Login         │    │ • JWT Auth      │    │ • Credentials   │
│ • Dashboard     │    │ • CORS          │    │ • Challenges    │
│ • Native WebAuthn│    │ • Validation    │    │ • TTL Indexes   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **WebAuthn** - FIDO2/WebAuthn implementation
- **MongoDB** - NoSQL database with Motor async driver
- **Pydantic v2** - Data validation and serialization
- **JWT** - JSON Web Token authentication
- **Python 3.13** - Latest Python features

### Frontend
- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **Native WebAuthn API** - Direct browser WebAuthn integration
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client with interceptors
- **React Router** - Client-side routing

### Database Schema
```javascript
// Users Collection
{
  "_id": ObjectId,
  "username": String,
  "user_id": String,
  "display_name": String,
  "created_at": Date,
  "last_login": Date
}

// Credentials Collection
{
  "_id": ObjectId,
  "user_id": String,
  "credential_id": String,
  "public_key": String,
  "sign_count": Number,
  "created_at": Date
}

// Challenges Collection (TTL: 5 minutes)
{
  "_id": ObjectId,
  "challenge": String,
  "username": String,
  "type": String, // "registration" | "authentication"
  "created_at": Date,
  "expires_at": Date
}
```

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **MongoDB Atlas** account (free tier available)
- **Modern browser** with WebAuthn support

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/authsys.git
cd authsys
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env
# Edit .env with your MongoDB connection string
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 4. Environment Configuration

Create `backend/.env`:
```env
# MongoDB Atlas connection string
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority&tls=true

# WebAuthn configuration - IMPORTANT: Set this to match your domain/IP
# For localhost development:
RP_ID=localhost

# For network IP (like 10.122.147.25):
# RP_ID=10.122.147.25

# For production domain:
# RP_ID=yourdomain.com

# Optional: Custom app name
RP_NAME=AuthSys WebAuthn Demo
```

### 5. Start Services

**Backend** (Terminal 1):
```bash
cd backend
# For localhost
uvicorn app.main:app --reload --port 8000

# For network access (replace with your IP)
RP_ID=10.122.147.25 uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**Frontend** (Terminal 2):
```bash
cd frontend
# For localhost
npm run dev

# For network access
npm run dev -- --host 0.0.0.0
```

### 6. Access Application

**Localhost:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Network Access (replace with your IP):**
- **Frontend**: http://10.122.147.25:5173
- **Backend API**: http://10.122.147.25:8000
- **API Docs**: http://10.122.147.25:8000/docs

## 📱 Usage Guide

### Registration Flow
1. **Navigate** to http://localhost:5173
2. **Click** "Register with Biometrics"
3. **Enter** your username/email
4. **Authenticate** with biometrics when prompted
5. **Success** - Redirected to dashboard

### Login Flow
1. **Navigate** to login page
2. **Enter** your username/email
3. **Click** "Login with Biometrics"
4. **Authenticate** with biometrics
5. **Success** - Access dashboard with JWT token

### Dashboard Features
- View user profile information
- See registration timestamp
- Logout functionality
- Protected route (requires JWT)

## 🔌 API Reference

### Authentication Endpoints

#### Start Registration
```http
POST /api/auth/register/begin
Content-Type: application/json

{
  "username": "user@example.com"
}
```

#### Complete Registration
```http
POST /api/auth/register/complete
Content-Type: application/json

{
  "username": "user@example.com",
  "credential": { /* WebAuthn credential response */ }
}
```

#### Start Login
```http
POST /api/auth/login/begin
Content-Type: application/json

{
  "username": "user@example.com"
}
```

#### Complete Login
```http
POST /api/auth/login/complete
Content-Type: application/json

{
  "username": "user@example.com",
  "credential": { /* WebAuthn credential response */ }
}
```

### User Endpoints

#### Get Current User
```http
GET /api/users/me
Authorization: Bearer <jwt_token>
```

## 🔧 Development

### Project Structure
```
authsys/
├── backend/
│   ├── app/
│   │   ├── models.py          # Pydantic models
│   │   ├── database.py        # MongoDB connection
│   │   ├── main.py           # FastAPI application
│   │   ├── routes/
│   │   │   ├── auth.py       # Authentication routes
│   │   │   └── user.py       # User routes
│   │   └── utils/
│   │       └── webauthn_utils.py  # WebAuthn utilities
│   ├── requirements.txt       # Python dependencies
│   └── .env                  # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── pages/           # Page components
│   │   ├── utils/           # Utility functions
│   │   └── App.jsx          # Main application
│   ├── package.json         # Node dependencies
│   └── vite.config.js       # Vite configuration
└── README.md
```

### Key Implementation Details

#### WebAuthn Challenge Flow
1. **Generate** cryptographic challenge on server
2. **Store** challenge in MongoDB with TTL
3. **Send** challenge to client
4. **Client** creates credential with biometrics
5. **Server** verifies challenge matches
6. **Store** credential for future authentication

#### Security Measures
- **Origin validation** prevents phishing
- **Challenge uniqueness** prevents replay attacks
- **TTL expiration** limits challenge lifetime
- **Public key cryptography** ensures authenticity
- **JWT tokens** for stateless sessions

## 🚀 Deployment

### Production Checklist
- [ ] Update `RP_ID` to production domain
- [ ] Use production MongoDB cluster
- [ ] Generate secure JWT secret
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS for production
- [ ] Set up monitoring and logging
- [ ] Implement rate limiting
- [ ] Add backup strategies

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🧪 Testing

### Manual Testing
1. **Registration** - Test with different browsers
2. **Login** - Verify biometric prompts work
3. **Cross-browser** - Test Chrome, Safari, Firefox
4. **Mobile** - Test on iOS/Android devices
5. **Error handling** - Test network failures

### Browser Compatibility
- ✅ Chrome 67+
- ✅ Safari 14+
- ✅ Firefox 60+
- ✅ Edge 18+
- ✅ iOS Safari 14+
- ✅ Android Chrome 70+

## 🔍 Troubleshooting

### Common Issues

#### "WebAuthn not supported"
- Use HTTPS or localhost
- Update to modern browser
- Enable biometrics in system settings

#### "Challenge mismatch"
- Clear browser data for localhost
- Restart backend server
- Check MongoDB connection

#### "Origin mismatch"
- Verify RP_ID matches domain
- Check CORS configuration
- Ensure consistent ports

#### "Biometric prompt not showing"
- Enable Touch ID/Face ID in settings
- Try different browser
- Check for browser permissions

## 📊 Performance

### Metrics
- **Registration time**: ~2-3 seconds
- **Login time**: ~1-2 seconds
- **Database queries**: Optimized with indexes
- **Memory usage**: Minimal with async operations
- **Concurrent users**: Scales with MongoDB Atlas

## 🔒 Security Considerations

### Best Practices Implemented
- ✅ No password storage
- ✅ Cryptographic challenge verification
- ✅ Origin validation
- ✅ Secure credential storage
- ✅ JWT token expiration
- ✅ HTTPS enforcement (production)
- ✅ Input validation and sanitization

### Security Audit Checklist
- [ ] Regular dependency updates
- [ ] Security headers implementation
- [ ] Rate limiting on endpoints
- [ ] Logging and monitoring
- [ ] Backup and recovery procedures

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **WebAuthn Specification** - W3C and FIDO Alliance
- **FastAPI** - Sebastian Ramirez and contributors
- **React Team** - Meta and contributors
- **MongoDB** - Database platform
- **Tailwind CSS** - Utility-first CSS framework

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/authsys/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/authsys/discussions)
- **Email**: your.email@example.com

---

**Built with ❤️ using WebAuthn, FastAPI, and React**
