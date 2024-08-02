import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment
from googletrans import Translator

def convert_audio_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_file = audio_file.name.split(".")[0] + ".wav"
    audio.export(wav_file, format="wav")
    return wav_file

def transcribe_speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        try:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("Could not understand audio")
        except sr.RequestError as e:
            st.error(f"Error: {str(e)}")

def translate_text(text, target_language):
    # Initialize the translator
    translator = Translator()

    # Translate the text
    translated_text = translator.translate(text, dest=target_language)

    return translated_text.text

def main():
    st.title("Speech to Text Converter")
    st.write("Upload an audio file and convert it to text.")

    uploaded_file = st.file_uploader("Choose an audio file", type=["wav", "mp3"])

    if uploaded_file is not None:
        file_details = {"Filename": uploaded_file.name, "FileType": uploaded_file.type}
        st.write(file_details)

        if uploaded_file.type == "audio/mp3":
            uploaded_file = convert_audio_to_wav(uploaded_file)

        # Choose target language
        target_language_options = ["en", "hi", "te", "ta"]  # Add more languages as needed
        target_language = st.selectbox("Select target language", target_language_options)

        if st.button("Convert"):
            transcribed_text = transcribe_speech_to_text(uploaded_file)

            if transcribed_text:
                translated_text = translate_text(transcribed_text, target_language)

                st.write("Translated Text:")
                st.write(translated_text)

if __name__ == "__main__":
    main()
