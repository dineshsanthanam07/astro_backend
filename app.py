from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from services.geocode import get_lat_lon
from services.astrology import get_chart
from services.gpt_service import generate_analysis, chat_followup

import uuid

app = FastAPI()

# ✅ ADD CORS HERE
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ For MVP (allow all)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store
sessions = {}


class BirthRequest(BaseModel):
    name: str
    day: int
    month: int
    year: int
    hour: int
    minute: int
    city: str


class ChatRequest(BaseModel):
    session_id: str
    message: str


@app.get("/")
def home():
    return {"message": "Astrology MVP Running 🚀"}


# 🔮 Generate Chart + Analysis
@app.post("/generate")
def generate(req: BirthRequest):
    try:
        lat, lon = get_lat_lon(req.city)

        payload = {
            "day": req.day,
            "month": req.month,
            "year": req.year,
            "hour": req.hour,
            "min": req.minute,
            "lat": lat,
            "lon": lon,
            "tzone": 5.5,
            "house_type": "placidus",
            "is_asteroids": "false"
        }

        chart = get_chart(payload)
        analysis = generate_analysis(chart)

        session_id = str(uuid.uuid4())

        sessions[session_id] = [
            {"role": "system", "content": "You are an astrologer."},
            {"role": "user", "content": f"My birth chart: {chart}"},
            {"role": "assistant", "content": analysis}
        ]

        return {
            "session_id": session_id,
            "analysis": analysis
        }

    except Exception as e:
        return {"error": str(e)}


# 💬 Follow-up Chat
@app.post("/chat")
def chat(req: ChatRequest):
    try:
        if req.session_id not in sessions:
            return {"error": "Invalid session"}

        sessions[req.session_id].append({
            "role": "user",
            "content": req.message
        })

        reply = chat_followup(sessions[req.session_id])

        sessions[req.session_id].append({
            "role": "assistant",
            "content": reply
        })

        return {"response": reply}

    except Exception as e:
        return {"error": str(e)}