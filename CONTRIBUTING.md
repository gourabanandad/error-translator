# Contributing to Error Translator

First off, thank you for considering contributing! This project relies on the community to map out the thousands of possible Python errors.

## How the Architecture Works
This project separates logic from data. 
* Do **not** edit `core.py` to add new errors.
* Do **not** manually edit `rules.json`. 

## How to Add a New Error Rule
We have built an AI-powered data pipeline to make adding rules incredibly fast and safe.

1. **Clone the repository and install dependencies:**
   `pip install -r requirements.txt`
2. **Set your Gemini API Key:**
   Get a free key from Google AI Studio and set it as an environment variable (`GEMINI_API_KEY`).
3. **Run the AI Builder:**
   `python builder.py`
4. **Approve or Edit:**
   The CLI will automatically find missing errors, generate the Regex pattern, write the explanation, and ask for your approval.
5. **Submit a Pull Request:**
   Once the tool saves your new rules to `rules.json`, commit your changes and open a Pull Request!

## Testing
Before submitting your Pull Request, ensure the core engine still works by running our test suite:
`pytest`