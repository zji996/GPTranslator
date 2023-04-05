import pysrt
import openai
import time
import json
import os
def translate_text(text, target_language, api_key, 
                   playrole, max_retries=3, retry_interval=3):
    openai.api_key = api_key
    retries = 0
    
    while retries < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"{playrole}"
                    },
                    {
                
                        "role": "user",
                        "content": f'Translate the following text to {target_language}: "{text}"'
                    }
                ]
            )
            translated_text = response['choices'][0]['message']['content']
            return translated_text.strip()
        except Exception as e:
            print(f"Error occurred while translating (attempt {retries + 1}): {e}")
            retries += 1
            if retries < max_retries:
                time.sleep(retry_interval)
            else:
                print(f"Translation failed after {max_retries} attempts. Waiting for breakpoint reconnect.")
                return None
def load_progress(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        with open(file_path, 'w') as f:
            json.dump({}, f)
        return {}

def save_progress(file_path, progress):
    with open(file_path, 'w') as f:
        json.dump(progress, f)

def load_glossary(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return {}

def find_glossary_terms(text, glossary):
    terms_found = []
    for term, definition in glossary.items():
        if term in text:
            terms_found.append((term, definition))
    return terms_found

def SubsTranslator(src, des, target, API, playrole='', relative_path='', progress_file='', glossary={}):
    if os.path.exists(des):
        subs = pysrt.open(des)
    else:
        subs = pysrt.open(src)
    progress = load_progress(progress_file)
    start_index = progress.get(relative_path, 0)
    for idx, sub in enumerate(subs[start_index:]):
        original_text = sub.text
        glossary_terms = find_glossary_terms(original_text, glossary)
        glossary_text = " ".join([f"{term}: {definition}" for term, definition in glossary_terms])
        playrole_with_glossary = f"{playrole} ,The following is a glossary: {glossary_text}" if glossary_terms else playrole
        if glossary_terms:
            print(f"Found glossary terms: {glossary_terms}")
        translated_text = translate_text(original_text, target, API, playrole_with_glossary).replace('。', ' ').replace('，', ' ').replace('\"', '').replace('“', '').replace('”', '')
        if translated_text:
            sub.text = f"{translated_text}\\n{original_text}"
            subs.save(des, encoding='utf-8')
            print(f"Translated subtitle index {start_index + idx}: {original_text} -> {translated_text}")
            progress[relative_path] = start_index + idx + 1
            save_progress(progress_file, progress)
        else:
            print(f"Failed to translate subtitle index {start_index + idx}: {original_text}")
        time.sleep(0.5)

    print(f"Translated {src} to {des}.")



