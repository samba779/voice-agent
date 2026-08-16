from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
from datetime import datetime

app = FastAPI(title="Voice Agent Webhook Handler")

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for call data (replace with database in production)
call_history = []

class CallData(BaseModel):
    message: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

@app.get("/")
async def root():
    return {
        "message": "Voice Agent Webhook Handler",
        "status": "running",
        "endpoints": {
            "webhook": "/api/call-webhook",
            "history": "/api/call-history",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/api/call-webhook")
async def handle_call_webhook(request: Request):
    """
    Handle webhook events from Vapi/Retell AI platform.
    Processes call completion events and extracts transcripts/summaries.
    """
    try:
        data = await request.json()
        print(f"\n{'='*50}")
        print(f"Webhook received at {datetime.now().isoformat()}")
        print(f"{'='*50}")
        
        # Check if the event is a call completion
        message = data.get("message", {})
        message_type = message.get("type", "")
        
        print(f"Event Type: {message_type}")
        
        if message_type == "end-of-call-report":
            # Extract call data
            transcript = message.get("transcript", "")
            summary = message.get("analysis", {}).get("summary", "")
            call_id = message.get("callId", "unknown")
            duration = message.get("endedReason", "unknown")
            
            call_record = {
                "call_id": call_id,
                "timestamp": datetime.now().isoformat(),
                "transcript": transcript,
                "summary": summary,
                "duration": duration,
                "raw_data": data
            }
            
            # Store call record
            call_history.append(call_record)
            
            print(f"\n✅ Call Completed - ID: {call_id}")
            print(f"📝 Summary: {summary}")
            print(f"\n📜 Full Transcript:")
            print("-" * 50)
            print(transcript)
            print("-" * 50)
            
            return {
                "status": "success",
                "call_id": call_id,
                "message": "Call data processed and stored"
            }
        
        elif message_type == "call-started":
            print(f"📞 Call started: {message.get('callId', 'unknown')}")
            return {"status": "success", "message": "Call started acknowledged"}
        
        elif message_type == "call-ended":
            print(f"📞 Call ended: {message.get('callId', 'unknown')}")
            return {"status": "success", "message": "Call ended acknowledged"}
        
        else:
            print(f"ℹ️ Other event: {message_type}")
            return {"status": "success", "message": f"Event {message_type} acknowledged"}
            
    except Exception as e:
        print(f"❌ Error processing webhook: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")

@app.get("/api/call-history")
async def get_call_history():
    """
    Retrieve all stored call records.
    """
    return {
        "total_calls": len(call_history),
        "calls": call_history
    }

@app.get("/api/call-history/{call_id}")
async def get_call_by_id(call_id: str):
    """
    Retrieve a specific call record by ID.
    """
    for call in call_history:
        if call["call_id"] == call_id:
            return call
    raise HTTPException(status_code=404, detail="Call not found")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Voice Agent Webhook Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("🔗 Webhook endpoint: http://localhost:8000/api/call-webhook")
    uvicorn.run(app, host="0.0.0.0", port=8000)
