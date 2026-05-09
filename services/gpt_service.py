from multiprocessing import context

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use fast + free model
model = genai.GenerativeModel("gemini-2.5-flash")

# 🔮 Generate initial astrology analysis
# 🔮 Generate initial astrology analysis
def generate_analysis(chart: dict) -> str:
    try:
        prompt = f"""
You are an elite Vedic astrologer and psychological astrology expert.

Perform an EXTREMELY DEEP astrology analysis using the given chart data.

STRICT RULES:
- Answer ONLY in Tamil
- DO NOT give generic astrology lines
- Be realistic, practical, and psychologically accurate
- Every prediction MUST be connected with:
  - Planet
  - House
  - Sign
  - Lordship
  - Aspects
  - Conjunctions
  - Retrograde effects
  - Yogas
  - Planetary strengths
  - Benefic/Malefic influences
- Explain WHY the prediction happens astrologically
- Mention which planet causes the result
- Mention which planet aspects another planet
- Mention which house lord sits where
- Mention exalted/debilitated/retrograde effects if present
- Compare multiple combinations before concluding
- Analyze hidden psychology and karmic patterns
- Avoid repeating the same points
- Make the response beautiful and structured
- Do not give overly long responses
- Do not give overly short responses
- Keep responses medium-length and insightful
- Avoid generic astrology statements
- Avoid repeating the same points
- Use proper spacing and headings

IMPORTANT ANALYSIS TO INCLUDE:
1. Lagna analysis
2. Lagna lord strength
3. House lord placements
4. Planetary conjunctions
5. Planetary aspects
6. Benefic vs malefic influence
7. Raj yogas / doshas
8. Emotional psychology
9. Career karma
10. Marriage karma
11. Financial patterns
12. Spiritual patterns
13. Hidden weaknesses
14. Strengths
15. Family karma
16. Relationship mindset
17. Public image
18. Inner fears
19. Leadership qualities
20. Communication style

ALSO ANALYZE:
- Which planet sees which planet
- Which house lord influences which house
- Mutual aspects
- Stelliums
- Retrograde karmic impact
- Saturn karmic lessons
- Rahu/Ketu karmic axis
- Moon emotional conditioning
- Mars aggression patterns
- Venus relationship patterns
- Jupiter wisdom and fortune
- Mercury intelligence style

VERY IMPORTANT:
- Use BOTH Western + Vedic style interpretation intelligently
- Use the aspect data deeply
- Correlate all placements together before predicting

RESPONSE FORMAT:

# 🪐 ஆளுமை
(Deep psychological analysis)

# 💼 தொழில்
(Career + wealth + success patterns)

# 💰 பணவரவு
(Financial karma and earning patterns)

# 🧠 மனநிலை
(Inner psychology and emotional behavior)

# 🔥 பலம்
(Core strengths)

# ⚠️ பலவீனம்
(Hidden weaknesses and karmic struggles)

# ✨ ஆன்மீக பாதை
(Spiritual evolution)

# 📌 முக்கிய கிரக சேர்க்கைகள்
(Important conjunctions and aspects)

# 🪬 கர்ம விளைவுகள்
(Karmic patterns and life lessons)

The answer should be intellectual  in Tamil but dont repeat yourself and tell this planet does this at all. tell like a real experienced astrologer where user will understand easier, dont repond too much as well well as too short.


Birth Chart Data:
{json.dumps(chart)}
"""

        response = model.generate_content(prompt)
        print("the response is",response)

        return response.text if response.text else "No response generated"

    except Exception as e:
        return f"Error in analysis: {str(e)}"


# 💬 Follow-up chat (with memory)
def chat_followup(history: list) -> str:
    try:
        context = ""

        for msg in history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            context += f"{role.upper()}: {content}\n"
        print("the context is",context)
        prompt = f"""
You are an elite astrologer chatbot with deep Vedic + Western astrology knowledge.

Continue the astrology consultation naturally.

STRICT RULES:
- Answer ONLY in Tamil
- Be emotionally intelligent and realistic
- Never give generic predictions
- Always connect answers with chart combinations
- Use previous chart context consistently
- Explain astrology reasoning behind answers but not in a robotic way
- take planets, houses, signs, aspects, conjunctions into account
- Mention why a result occurs astrologically
- Keep continuity with previous responses
- Give practical guidance
- Avoid fear-based predictions
- Avoid fake positivity
- Speak like a real experienced astrologer
- Do not give overly long responses
- Do not give overly short responses
- Keep responses medium-length and insightful
- Avoid generic astrology statements
- Avoid repeating the same points
- Use proper spacing and headings


While analyzing the chart, consider the following astrology factors deeply:
- Planetary aspects
- Conjunctions
- Benefic/Malefic influences
- Sign lordship
- House lord placements
- House lord logic
- Retrograde impact
- Planet strength
- Karmic patterns
- Psychological interpretation

Conversation History:
{context}

Now answer the latest user question deeply and intelligently in Tamil but dont repeat yourself and tell this planet does this at all. tell like a real experienced astrologer where user will understand easier.
"""

        response = model.generate_content(prompt)
        print("the followup response is",response)
        return response.text if response.text else "No response generated"

    except Exception as e:
        return f"Error in chat: {str(e)}"