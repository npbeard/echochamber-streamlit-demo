import streamlit as st
from echochamber import Persona, NoirVoice, SciFiVoice, TherapyVoice
from echochamber.utils import EngineConfig

st.title("🌌 echochamber demo")

text = st.text_area("Enter text", "The weather is quite rainy today.")
voice_name = st.selectbox("Voice", ["noir", "scifi", "therapy"])
layers = st.slider("Layers (recursion)", 1, 5, 1)
chaos = st.checkbox("Chaos mode (regex)", value=False)
include_time = st.checkbox("Include time", value=True)
chunk_size = st.slider("Chunk size (generator streaming)", 5, 40, 16)

intensity = st.slider("Chaos intensity", 1, 3, 1)

voice_map = {
    "noir": NoirVoice(),
    "scifi": SciFiVoice(),
    "therapy": TherapyVoice(),
}
voice = voice_map[voice_name]

cfg = EngineConfig(include_time=include_time, chaos=chaos)

persona = Persona(name="StreamlitUser", voice=voice, config=cfg)
persona.add_tags("streamlit")

if st.button("Echo"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        placeholder = st.empty()
        output = ""
        for chunk in persona.echo(text, chunk_size=chunk_size, layers=layers, intensity=intensity):
            output += chunk
            placeholder.markdown(output)