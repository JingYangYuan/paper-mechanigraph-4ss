import os
import glob
import time
import re
from google import genai
from google.genai import types

WORKSPACE_DIR = os.environ.get("WORKSPACE_DIR") or os.getcwd()
SKILL_MD_PATH = os.path.join(os.path.dirname(__file__), "..", "SKILL.md")
SOURCE_DIR = os.environ.get("SOURCE_DIR") or os.path.join(WORKSPACE_DIR, "source_images")
OUTPUT_DIR = os.environ.get("OUTPUT_DIR") or os.path.join(WORKSPACE_DIR, "svg_replications")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_skill_prompt():
    with open(SKILL_MD_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def extract_svg(text):
    match = re.search(r'```xml\n(.*?)\n```', text, re.DOTALL)
    if match: return match.group(1)
    match = re.search(r'```svg\n(.*?)\n```', text, re.DOTALL)
    if match: return match.group(1)
    if '<svg' in text and '</svg>' in text:
        return text[text.find('<svg'):text.find('</svg>')+6]
    return text

def process_image(client, image_path, skill_prompt):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    print(f"[{time.strftime('%H:%M:%S')}] Processing {base_name}...")
    
    prompt = f"""
    You are an expert academic SVG generator.
    Strictly apply the following rules (NO titles, NO annotations, STRICT Black/White/Grayscale, ABSOLUTE centering, big readable fonts):
    
    {skill_prompt}
    
    Replicate the theoretical mechanism / framework diagram from the provided image into a pure vector SVG.
    Output ONLY the raw SVG code inside ```xml ``` blocks.
    """
    
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
            
        response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/png' if image_path.lower().endswith('.png') else 'image/jpeg'),
                prompt
            ]
        )
        
        svg_content = extract_svg(response.text)
        
        # Validation Loop
        for loop in range(2):
            val_prompt = f"""
            Review your SVG code against the strict rules:
            1. Is it centered in the viewBox without skewing to the top-left?
            2. Are fonts large enough (20-24px for titles, 16-18px for nodes)?
            3. Are there ANY overlapping texts, borders, or arrows cutting text?
            4. Does it contain ANY forbidden titles or annotations?
            5. Is it STRICTLY black, white, and grayscale?
            
            If flawless, reply: <FLAWLESS>
            Otherwise, output the FULL corrected SVG code in ```xml ```.
            
            Current SVG:
            ```xml
            {svg_content}
            ```
            """
            val_res = client.models.generate_content(model='gemini-2.5-pro', contents=[val_prompt])
            if "<FLAWLESS>" in val_res.text:
                break
            else:
                svg_content = extract_svg(val_res.text)
                
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        out_svg = os.path.join(OUTPUT_DIR, f"{base_name}_replicated.svg")
        with open(out_svg, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"  -> Generated: {out_svg}")
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

def main():
    client = genai.Client()
    skill_prompt = load_skill_prompt()
    images = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.png")) + glob.glob(os.path.join(SOURCE_DIR, "*.jpg")))
    print(f"Found {len(images)} images in {SOURCE_DIR}.")
    for img in images:
        process_image(client, img, skill_prompt)
        time.sleep(2)

if __name__ == "__main__":
    main()
