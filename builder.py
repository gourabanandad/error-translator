import json
import os
from google import genai # <-- NEW SDK IMPORT

# ANSI Colors for a beautiful admin experience
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
RESET = '\033[0m'

# Configure the new Gemini API Client
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    print(f"{YELLOW} Warning: GEMINI_API_KEY environment variable not set.{RESET}")
    print("Please set it to use the AI auto-generation feature.\n")
    client = None
else:
    client = genai.Client(api_key=api_key) # <-- NEW CLIENT INITIALIZATION

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def ask_ai_for_rule(error_name, description):
    """Asks Gemini to generate the regex and explanations."""
    if not client:
        return None
        
    print(f"{MAGENTA} Asking AI to generate rules...{RESET}")
    
    prompt = f"""
    You are an expert Python developer building an error translation tool.
    I need a regex pattern, a simple explanation, and a suggested fix for this Python error:
    
    Error Name: {error_name}
    Official Description: {description}
    
    Return ONLY a valid JSON object with exactly these three keys. Do not include markdown formatting or backticks.
    {{
        "pattern": "The regex pattern to match this error string in a traceback (escape special characters)",
        "explanation": "A beginner-friendly explanation of why this happens.",
        "fix": "Actionable advice on how to fix it."
    }}
    """
    
    try:
        # <-- NEW GENERATION CALL using the latest model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        # Strip any accidental markdown formatting the LLM might include
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_text)
    except Exception as e:
        print(f"{YELLOW}AI Generation failed: {e}{RESET}")
        return None

def main():
    print(f"{CYAN}===  AI-Powered Rule Builder ==={RESET}\n")
    
    rules_data = load_json('error_translator/rules.json')
    scraped_data = load_json('scraped_errors_database.json')
    
    if not rules_data or not scraped_data:
        print("Error: Could not find databases.")
        return

    existing_patterns = [rule["pattern"] for rule in rules_data["rules"]]
    added_count = 0

    for scraped_error in scraped_data:
        error_name = scraped_error["error_name"]
        
        already_exists = any(error_name in pattern for pattern in existing_patterns)
        
        if not already_exists:
            print(f"{YELLOW} Missing Rule for: {error_name}{RESET}")
            print(f"Description: {scraped_error['official_description']}\n")
            
            ai_draft = ask_ai_for_rule(error_name, scraped_error['official_description'])
            
            if ai_draft:
                print(f"{CYAN}--- AI Generated Draft ---{RESET}")
                print(f"Pattern:     {ai_draft.get('pattern', '')}")
                print(f"Explanation: {ai_draft.get('explanation', '')}")
                print(f"Fix:         {ai_draft.get('fix', '')}")
                print(f"{CYAN}--------------------------{RESET}\n")
                
                choice = input("Accept AI draft? (y/n/edit/quit): ").strip().lower()
            else:
                choice = input("No AI draft available. Add manually? (y/n/quit): ").strip().lower()
            
            if choice == 'quit':
                break
            elif choice == 'y' and ai_draft:
                rules_data["rules"].append(ai_draft)
                existing_patterns.append(ai_draft["pattern"])
                added_count += 1
                print(f"{GREEN} Rule approved and added!{RESET}\n")
            elif choice == 'edit' or (choice == 'y' and not ai_draft):
                print("\n" + "-"*40)
                pattern = input(f"1. Pattern (AI suggested: {ai_draft.get('pattern', '') if ai_draft else ''}): ") or (ai_draft['pattern'] if ai_draft else '')
                explanation = input(f"2. Explanation (AI suggested: {ai_draft.get('explanation', '') if ai_draft else ''}): ") or (ai_draft['explanation'] if ai_draft else '')
                fix = input(f"3. Fix (AI suggested: {ai_draft.get('fix', '') if ai_draft else ''}): ") or (ai_draft['fix'] if ai_draft else '')
                
                rules_data["rules"].append({
                    "pattern": pattern,
                    "explanation": explanation,
                    "fix": fix
                })
                existing_patterns.append(pattern)
                added_count += 1
                print(f"{GREEN} Rule saved!{RESET}\n")
            else:
                print("Skipping...\n")

    if added_count > 0:
        save_json('error_translator/rules.json', rules_data)
        print(f"{GREEN} Successfully saved {added_count} new rules to rules.json!{RESET}")
    else:
        print("No new rules added.")

if __name__ == "__main__":
    main()