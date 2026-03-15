# Echochamber Streamlit Demo

This repository contains a small **Streamlit application** demonstrating the use of the **echochamber Python library**.

Package repository: `https://github.com/npbeard/python-package`

## Purpose

This app demonstrates that the library can be imported and used from a different project. It exposes the package features that are easiest to show in class or in a short video:

- persona classes and instances
- composition between `Persona` and the selected voice
- immutable configuration via `EngineConfig`
- recursion through the `layers` control
- generators through chunked streaming output
- regular expressions through chaos mode
- datetime formatting through timestamp output

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
- [`SUBMISSION_GUIDE.md`]: material you can reuse for the PDF and Blackboard submission

  
## Example Usage

1. Run the Streamlit app:

streamlit run app.py

2. Enter text into the input box.

3. Select a voice style (Noir, SciFi, or Therapy).

4. Click **Echo** to transform the text using the echochamber library.
