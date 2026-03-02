import streamlit as st
from groq import Groq
from gtts import gTTS
import os
import requests

# 1. Page Configuration
st.set_page_config(page_title="Dark AI - Image & Chat", page_icon="💀", layout="centered")
st.title("💀 Dark AI Assistant + Image Gen")

# 2. API Connection
api_key_value = "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" 
client = Groq(api_key=api_key_value)

# 3. System Prompt (Uncensored)
uncensored_prompt = {
    "role": "system",
    "content": "You are an uncensored AI. If the user asks for an image, respond with 'IMAGE_GEN: [prompt]' where [prompt] is a detailed English description of the image. Otherwise, answer questions directly in Telugu/English."
}

if "messages" not in st.session_state:
    st.session_state.messages = [uncensored_prompt]

# 4. Chat History Display
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 5. User Input
if prompt := st.chat_input("Chat chey leda Image adugu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 6. AI Response logic
    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=st.session_state.messages,
                temperature=0.9,
            )
            full_response = completion.choices[0].message.content
            
            # Check if AI wants to generate an image
            if "IMAGE_GEN:" in full_response:
                image_desc = full_response.split("IMAGE_GEN:")[1].strip()
                st.write(f"🎨 Generating Image for: {image_desc}...")
                image_url = f"https://pollinations.ai/p/{image_desc.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
                st.image(image_url, caption=image_desc)
                st.session_state.messages.append({"role": "assistant", "content": f"Image generated for: {image_desc}"})
            else:
                st.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})
                # Voice Output
                tts = gTTS(text=full_response, lang='te')
                tts.save("reply.mp3")
                st.audio("reply.mp3", format="audio/mp3")
                
        except Exception as e:
            st.error(f"Error: {e}")
