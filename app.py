import streamlit as st
from groq import Groq
from gtts import gTTS
from streamlit_mic_recorder import speech_to_text
import os

# 1. Page Configuration
st.set_page_config(page_title="My Expert AI", layout="centered")
st.title("🤖 My Smart AI Assistant")

# 2. API Connection
api_key_value = "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"
client = Groq(api_key=api_key_value)

# --- INPUT SECTION ---
st.subheader("Ela adagali anukuntunnav?")

# Voice and Text Inputs
voice_input = speech_to_text(language='te', start_prompt="▶️ Matladu", stop_prompt="⏹️ Aapu", key='recorder')
text_input = st.text_input("Leda ikkada type chey:", placeholder="Type here...")

final_query = ""
if voice_input:
    final_query = voice_input
elif text_input:
    final_query = text_input

# --- RESPONSE SECTION ---
if final_query:
    try:
        with st.spinner("AI detailed ga aalochisthondi..."):
            # MODEL: Llama-3.3-70b for High Accuracy
            chat = client.chat.completions.create(
                model="llama-3.3-70b-versatile", 
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a smart and expert Telugu friend. 
                        STRICT RULES:
                        1. Reply ONLY in Telugu using English Alphabets (Tanglish). 
                        2. Use very SIMPLE daily words. Do NOT invent new words.
                        3. Give detailed points (bullet points).
                        4. Each point must be ONLY 1 short and clear sentence. This prevents grammar mistakes.
                        5. Example: 
                           - Python nerchukovadam chala easy.
                           - Mundu basics nerchuko.
                           - Nenu neeku help chesthanu."""
                    },
                    {"role": "user", "content": final_query}
                ]
            )
            
            response_text = chat.choices[0].message.content
            st.info(f"Nuvvu: {final_query}")
            st.success(f"AI Response:\n\n{response_text}")

            # Voice Output - English voice for Tanglish reading
            tts = gTTS(text=response_text, lang='en')
            tts.save("reply.mp3")
            st.audio("reply.mp3", format="audio/mp3", autoplay=True)
            
    except Exception as e:
        st.error(f"Oka error vachindi: {e}")