import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration (Website ka Title aur Layout)
st.set_page_config(page_title="Dual AI Agents Portal", page_icon="🤖", layout="centered")

# 2. Gemini Client Setup (Aapki API Key)
client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# --- UI Header ---
st.title("🤖 Dual AI Agents Portal")
st.write("Apna pasandida AI Agent chunein aur live chat shuru karein!")
st.markdown("---")

# 3. Sidebar me Agent Selector
st.sidebar.title("Configuration")
agent_choice = st.sidebar.radio(
    "Select AI Agent:",
    ("Medical Help Agent 🩺", "Student Science Agent (Class 12) 🧪")
)

# 4. System Prompts Definition
if "Medical Help Agent" in agent_choice:
    system_prompt = (
        "You are a helpful and empathetic Medical Assistant. Your goal is to explain medical concepts, "
        "symptoms, and general health advice in simple, easy-to-understand Hindi/English (Hinglish). "
        "Always include a friendly greeting and firmly remind the user to consult a real doctor for professional advice."
    )
    placeholder_text = "Apni health ya medical query yahan likhein..."
    welcome_msg = "🩺 Medical Assistant active hai. Main aapki kya madad kar sakta hoon?"
else:
    system_prompt = (
        "You are a brilliant and fun Science Teacher for school students up to Class 12. "
        "Your job is to explain complex science topics (Physics, Chemistry, Biology) in a very easy, "
        "relatable, and engaging way using everyday examples. Use simple Hinglish/Hindi-English mix. "
        "Break down tough concepts into simple points."
    )
    placeholder_text = "Science ka koi bhi topic ya sawaal yahan likhein..."
    welcome_msg = "🧪 Science Teacher active hai. Class 12 tak ka koi bhi topic puchiye!"

# 5. Chat History Maintain Karna (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Agar agent badla, toh purani chat clear karne ke liye (Optional)
if "last_agent" not in st.session_state:
    st.session_state.last_agent = agent_choice
elif st.session_state.last_agent != agent_choice:
    st.session_state.messages = []
    st.session_state.last_agent = agent_choice

# Screen par welcome message dikhana
st.chat_message("assistant").write(welcome_msg)

# Purane messages screen par display karna
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 6. User Input aur Response Logic
if user_query := st.chat_input(placeholder=placeholder_text):
    # User ka message screen par dikhayein aur history me save karein
    st.chat_message("user").write(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # AI response generate karein
    with st.spinner("AI soch raha hai..."):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_query,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                )
            )
            ai_reply = response.text
            
            # AI ka reply screen par dikhayein aur history me save karein
            st.chat_message("assistant").write(ai_reply)
            st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            
        except Exception as e:
            st.error(f"Error aaya bhai: {e}")