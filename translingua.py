import streamlit as st
from googletrans import Translator, LANGUAGES
import speech_recognition as sr
from gtts import gTTS
import os

# Initialize Translator and Speech Recognizer
translator = Translator()
recognizer = sr.Recognizer()

# Streamlit UI Configuration
st.set_page_config(page_title="TransLingua", page_icon="🌍", layout="wide")

# Page Title and Description
st.markdown("<h1 style='text-align: center;'>🌍 TransLingua: AI-Powered Translator</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>A seamless tool for text, speech, and audio translation</h4>", unsafe_allow_html=True)

# Sidebar for Language Selection
st.sidebar.header("🌐 Language Settings")
language_names = {code: name.capitalize() for code, name in LANGUAGES.items()}
selected_lang = st.sidebar.selectbox("Select Target Language:", options=list(language_names.keys()), format_func=lambda x: language_names[x])

# --- MAIN LAYOUT ---
col1, col2 = st.columns(2)

# 📝 Text Translation Section
with col1:
    st.subheader("✏ Text Translation")
    text_input = st.text_area("Enter text to translate:", height=150)
    
    if st.button("🔄 Translate"):
        if text_input.strip():
            translated_text = translator.translate(text_input, dest=selected_lang).text
            st.text_area("📖 Translated Text:", translated_text, height=150)
            
            # Convert translated text to speech automatically
            tts = gTTS(text=translated_text, lang=selected_lang)
            tts.save("translated_speech.mp3")
            st.audio("translated_speech.mp3")
        else:
            st.warning("⚠ Please enter text to translate.")

# 🎤 Speech-to-Text Section
with col2:
    st.subheader("🎙 Speech to Text & Translate")
    if st.button("🎤 Start Recording"):
        with sr.Microphone() as source:
            st.info("🎙 Speak Now...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            try:
                spoken_text = recognizer.recognize_google(audio)
                st.text_area("🗣 Recognized Speech:", spoken_text, height=100)
                
                # Automatically translate speech
                translated_speech = translator.translate(spoken_text, dest=selected_lang).text
                st.text_area("📖 Translated Speech:", translated_speech, height=150)
                
                # Convert translated speech to speech
                tts = gTTS(text=translated_speech, lang=selected_lang)
                tts.save("translated_speech.mp3")
                st.audio("translated_speech.mp3")

            except sr.UnknownValueError:
                st.error("❌ Could not understand the audio.")
            except sr.RequestError:
                st.error("❌ Speech Recognition service error.")

# 📝 Improved Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>🚀 Built with ❤ using Streamlit & AI</p>", unsafe_allow_html=True)
