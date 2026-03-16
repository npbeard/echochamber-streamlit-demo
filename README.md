# Echochamber Streamlit Demo

This repository contains a small **Streamlit application** demonstrating the use of the **echochamber Python library** as a multi-persona conversation simulator.

Package repository: `https://github.com/npbeard/python-package`

## Purpose

This app demonstrates that the library can be imported and used from a different project. It exposes the package features that are easiest to show in class or in a short video:

- persona classes and instances
- composition between `Conversation`, `Persona`, and the selected voice
- immutable configuration via `EngineConfig`
- recursion through the `layers` control
- generators through chunked transcript replay
- regular expressions through chaos mode
- datetime formatting through timestamp output
- collections, JSON persistence, and transcript statistics

## Installation

Create and activate a virtual environment if needed, then install the demo requirements:

```bash
pip install -r requirements.txt
```

If you prefer installing manually, use:

```bash
pip install streamlit
pip install --extra-index-url https://test.pypi.org/simple/ echochamber
```

## Run The App

```bash
streamlit run app.py
```

## Files In This Repo

- [`app.py`]: Streamlit interface that imports and uses the package
- [`requirements.txt`]: demo app dependencies

## Example Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Enter or select a discussion topic.

3. Select one or more persona voices.

4. Click **Run Simulation** to generate a transcript, replay it, and inspect the structured results.
