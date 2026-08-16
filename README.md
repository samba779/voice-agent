# Browser-Based Voice Agent

A complete voice agent system using WebRTC, Vapi AI orchestration, and FastAPI backend.

## 🏗️ Architecture

```
Frontend (Web Browser)
    ↓ WebRTC Audio
Vapi/Retell AI Platform
    ↓ Webhook Events
Backend (FastAPI)
```

## 📁 Project Structure

```
voice-agent/
├── backend/
│   └── main.py          # FastAPI webhook handler
├── frontend/
│   └── index.html       # Web interface with Vapi SDK
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## 🚀 Setup Guide

### Step 1: Get Vapi Credentials

1. Sign up at [vapi.ai](https://vapi.ai)
2. Create an Assistant with your custom system prompt
3. Link your voice model (ElevenLabs or similar)
4. Get your:
   - **Public Web SDK Key** (for frontend)
   - **Assistant ID** (for frontend)
   - **Private API Key** (for backend, if needed)

### Step 2: Backend Setup

```bash
# Navigate to project
cd C:\Users\samba\CascadeProjects\voice-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
python backend\main.py
```

Backend will run on: `http://localhost:8000`

### Step 3: Configure Frontend

Edit `frontend/index.html` and replace:
```javascript
const CONFIG = {
    apiKey: "YOUR_PUBLIC_WEB_SDK_KEY",  // Replace with your key
    assistantId: "YOUR_ASSISTANT_ID"    // Replace with your ID
};
```

### Step 4: Expose Backend (for Webhooks)

During development, use ngrok to expose your local backend:

```bash
# Install ngrok (if not installed)
# Download from: https://ngrok.com/download

# Start ngrok
ngrok http 8000
```

Copy the ngrok URL (e.g., `https://abc123.ngrok.io`) and set it as your webhook URL in Vapi dashboard:
- Webhook URL: `https://abc123.ngrok.io/api/call-webhook`

### Step 5: Test Frontend Locally

Open `frontend/index.html` in your browser:
```bash
# Simply double-click the file or:
start frontend\index.html
```

Or use a simple HTTP server:
```bash
python -m http.server 3000 --directory frontend
```

Then open: `http://localhost:3000`

## 🌐 Deploy Frontend (Production)

### Option 1: Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy from frontend directory
cd frontend
vercel
```

### Option 2: Netlify

```bash
# Drag and drop the frontend folder to netlify.com
# Or use Netlify CLI
npm install -g netlify-cli
cd frontend
netlify deploy
```

## 🔧 Backend Endpoints

- `GET /` - Server info
- `GET /health` - Health check
- `POST /api/call-webhook` - Receive Vapi webhooks
- `GET /api/call-history` - View all call records
- `GET /api/call-history/{call_id}` - View specific call

## 📱 Testing on Mobile

1. Deploy frontend to Vercel/Netlify
2. Open the URL on your phone browser
3. Click "Start" and grant microphone permission
4. Talk to your AI assistant
5. Check backend logs for transcript and summary

## 🔒 Security Notes

- Never commit API keys to git
- Use environment variables for sensitive data
- In production, restrict CORS to your frontend domain
- Use HTTPS for all endpoints in production

## 🛠️ Troubleshooting

**Microphone not working?**
- Check browser permissions
- Try Chrome/Firefox instead of Safari
- Ensure HTTPS is used (required for microphone access)

**Webhook not receiving data?**
- Verify ngrok is running
- Check webhook URL in Vapi dashboard
- Look at backend console for errors

**Audio quality issues?**
- Check internet connection
- Verify voice model settings in Vapi
- Test with different browsers

## 📝 Customization

### Change Assistant Personality

Edit your assistant in Vapi dashboard with a custom system prompt:
```
You are a helpful personal assistant named Alex. 
You are friendly, concise, and always ready to help.
```

### Add Database Storage

Replace the in-memory `call_history` list with a real database:
- SQLite for simple projects
- PostgreSQL for production
- MongoDB for flexible schemas

### Add Email Notifications

Extend the webhook handler to send emails when calls complete:
```python
import smtplib
# Add email sending logic in handle_call_webhook
```

## 📚 Resources

- [Vapi Documentation](https://docs.vapi.ai)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [WebRTC Guide](https://webrtc.org)

## 🎯 Next Steps

1. ✅ Set up Vapi account and credentials
2. ✅ Run backend locally with ngrok
3. ✅ Configure frontend with your keys
4. ✅ Test locally in browser
5. ✅ Deploy frontend to Vercel
6. ✅ Test on mobile device
7. ✅ Add database for persistent storage
8. ✅ Add email/SMS notifications

---

Built with ❤️ using WebRTC, Vapi AI, and FastAPI
