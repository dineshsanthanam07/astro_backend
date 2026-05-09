from multiprocessing import context

import google.generativeai as genai
import os
import json
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use fast + free model
model = genai.GenerativeModel("gemini-2.5-flash")

log = logging.getLogger(__name__)

# 🔮 Generate initial astrology analysis
# 🔮 Generate initial astrology analysis
# 🔮 INITIAL REPORT GENERATION
def generate_analysis(chart: dict) -> str:
    try:
        prompt = f"""
        You are a professional astrologer.

        Analyze the given birth chart deeply.

        Rules:
        - Answer strictly in Tamil
        - Avoid generic statements
        - Take Laknam as 1 st house and analyze based on that.
        - Use planet + house + sign combinations
        - Use Planetary houses, yogas, aspects, exaltation, debilitation, retrograde, conjunctions, house lordship, karmic, oppositions, and malefics for deeper insights.
        - Be consistent with the chart data
        - Use the exact chart data provided, do not make assumptions
        - The explanation should be like Professional Astrologer explaining to a client, not like a textbook or robot
        - Speak naturally like real astrologer
        - Don't mention generic lines like "you are a good person" or "you have a strong mind". Be specific and practical in your analysis. and also dont mention degree of the planets like bot be like a real astrologer, dont tell the planatery position on everything just give a explanation as a real astrologer explains to normal people and give practical guidance based on the chart.
        Provide a detailed report covering:
        1. Deatils of rasi, laknam and each planet's position.
        2. Personality
        3. Career
        4. Strengths
        5. Weaknesses

        Chart:
        {json.dumps(chart)}
        """

        response = model.generate_content(prompt)
        log.info("the response from gemini api is",response.text)
        return response.text if response.text else "No response generated"

    except Exception as e:
        return f"Error: {str(e)}"


def chat_followup(history: list) -> str:
    try:
        context = ""
        for msg in history:
            context += f"{msg['role']}: {msg['content']}\n"

        prompt = f"""
        You are an  Professional astrologer chatbot.

        Continue conversation.

        Rules:
        - Answer only in Tamil
        - Be consistent with previous analysis
        - Use planet + house + sign combinations
        - Use Planetary aspects,retrograde, conjunctions, lord house, oppositions, and malefics for deeper insights.
        - Be consistent with the chart data
        - Use the exact chart data provided, do not make assumptions
        - The explanation should be like Professional Astrologer explaining to a client, not like a textbook or 
        -Speak naturally like real astrologer
        - Give practical guidance
        - Avoid generic lines
        - Mention astrology reasoning naturally
        Conversation:
        {context}
        """
        log.info("the conversation history is",context)
        response = model.generate_content(prompt)
        log.info("the response from gemini api is",response.text)
        return response.text if response.text else "No response generated"

    except Exception as e:
        return f"Error: {str(e)}"