from __future__ import annotations

import importlib
import json
import time

import streamlit as st  # type: ignore

try:
    echochamber = importlib.import_module("echochamber")
    echochamber_utils = importlib.import_module("echochamber.utils")

    Conversation = echochamber.Conversation
    NoirVoice = echochamber.NoirVoice
    Persona = echochamber.Persona
    SciFiVoice = echochamber.SciFiVoice
    TherapyVoice = echochamber.TherapyVoice
    EngineConfig = echochamber_utils.EngineConfig
except ModuleNotFoundError:
    st.set_page_config(
        page_title="echochamber simulator", page_icon="🌌", layout="wide"
    )
    st.error(
        "The `echochamber` package is not installed. "
        "Install the library from TestPyPI before running this app."
    )
    st.code(
        "pip install --extra-index-url https://test.pypi.org/simple/ "
        "echochamber"
    )
    st.stop()

st.set_page_config(
    page_title="echochamber simulator", page_icon="🌌", layout="wide"
)

VOICE_MAP = {
    "noir": NoirVoice,
    "scifi": SciFiVoice,
    "therapy": TherapyVoice,
}

EXAMPLES = {
    "Launch strategy": "What would make a new digital storytelling tool memorable to first-time users?",
    "AI ethics debate": "Should AI personas preserve the exact tone of the original author?",
    "Deadline triage": "We have one evening left. What should we prioritize for the submission?",
}


def build_persona(name: str, voice_name: str, include_time: bool, chaos: bool) -> Persona:
    """Create a persona tagged for Streamlit-based simulations."""
    config = EngineConfig(include_time=include_time, chaos=chaos)
    persona = Persona(name=name, voice=VOICE_MAP[voice_name](), config=config)
    persona.add_tags("streamlit", "conversation", voice_name)
    if chaos:
        persona.add_tags("regex")
    if include_time:
        persona.add_tags("datetime")
    return persona


st.title("🌌 echochamber simulator")
st.caption(
    "A separate Streamlit project that turns the published package into a "
    "multi-persona conversation lab."
)

with st.sidebar:
    st.header("Simulation Controls")
    example_name = st.selectbox("Scenario", list(EXAMPLES))
    topic = st.text_area("Conversation topic", value=EXAMPLES[example_name], height=120)
    selected_voices = st.multiselect(
        "Participants",
        options=["noir", "scifi", "therapy"],
        default=["noir", "scifi", "therapy"],
    )
    rounds = st.slider("Rounds", min_value=1, max_value=4, value=2)
    layers = st.slider("Recursion layers", min_value=1, max_value=4, value=1)
    intensity = st.slider("Chaos intensity", min_value=1, max_value=3, value=2)
    include_time = st.checkbox("Include timestamps inside persona output", value=False)
    chaos = st.checkbox("Chaos mode", value=False)
    animate = st.checkbox("Animate transcript replay", value=True)


def build_conversation() -> Conversation:
    conversation = Conversation(title=topic[:40] or "Streamlit simulation")
    for index, voice_name in enumerate(selected_voices, start=1):
        persona = build_persona(
            name=f"{voice_name.title()}-{index}",
            voice_name=voice_name,
            include_time=include_time,
            chaos=chaos,
        )
        conversation.add_personas(persona)
    return conversation


left_col, right_col = st.columns([2.2, 1.2])

with left_col:
    st.subheader("Transcript")
    st.write(
        "Run a simulation to generate a transcript, replay it in chunks, and export the session as JSON."
    )
    if st.button("Run Simulation", type="primary", use_container_width=True):
        if not topic.strip():
            st.warning("Please enter a topic before running the simulation.")
        elif not selected_voices:
            st.warning("Select at least one participant.")
        else:
            conversation = build_conversation()
            conversation.simulate(
                topic,
                rounds=rounds,
                layers=layers,
                intensity=intensity,
            )
            st.session_state["conversation_payload"] = conversation.to_dict()
            st.session_state["conversation_replay"] = list(conversation.replay(chunk_size=80))

    payload = st.session_state.get("conversation_payload")
    replay_chunks = st.session_state.get("conversation_replay", [])
    if payload:
        if animate:
            placeholder = st.empty()
            streamed = ""
            for chunk in replay_chunks:
                streamed += chunk
                placeholder.code(streamed)
                time.sleep(0.02)
        else:
            st.code("".join(replay_chunks))

        st.download_button(
            "Download session JSON",
            data=json.dumps(payload, indent=2),
            file_name="echochamber_session.json",
            mime="application/json",
            use_container_width=True,
        )

with right_col:
    st.subheader("Analysis")
    payload = st.session_state.get("conversation_payload")
    if payload:
        stats = payload["stats"]
        st.metric("Messages", stats["message_count"])
        st.write("Participants", ", ".join(stats["participants"]))
        st.write("Messages by speaker", stats["messages_by_speaker"])
        st.write("Top words", stats["top_words"])
        st.subheader("Transcript objects")
        st.json(payload["history"])
    else:
        st.info("Run a simulation to see transcript statistics and structured message data.")

    st.subheader("Concepts on display")
    st.markdown(
        """
        - `Conversation`, `Persona`, and `Message` show classes, instances, and composition.
        - The transcript replay uses generators and iterables.
        - Persona configuration uses immutable dataclasses and keyword arguments.
        - Session export uses paths, JSON, and collections.
        - Multi-round simulation adds recursion, loops, and richer object state.
        """
    )

    st.subheader("How to run")
    st.code("streamlit run app.py")
