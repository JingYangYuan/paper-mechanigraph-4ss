import os
import glob
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from google import genai
from google.genai import types

def analyze_image(client, img_path):
    prompt = "Analyze this academic diagram. What is the fundamental layout/topology (e.g., pipeline, circular, hierarchical, matrix, coordinate system, network)? Reply with a 3-word summary of the layout structure."
    try:
        with open(img_path, "rb") as f:
            image_bytes = f.read()
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type='image/png' if img_path.lower().endswith('.png') else 'image/jpeg'),
                prompt
            ]
        )
        return os.path.basename(img_path), response.text.strip()
    except Exception as e:
        return os.path.basename(img_path), f"Error: {str(e)}"

def main():
    print("Starting layout extraction for all images...")
    client = genai.Client()
    
    img_dir = r"C:\Users\YJY\Desktop\draw-mechanism\source_images"
    images = glob.glob(os.path.join(img_dir, "*.png")) + glob.glob(os.path.join(img_dir, "*.jpg"))
    
    if not images:
        print("No images found in source_images!")
        return

    print(f"Found {len(images)} images. Analyzing...")
    results = {}
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(analyze_image, client, img): img for img in images}
        for i, future in enumerate(as_completed(futures)):
            img_name, layout = future.result()
            results[img_name] = layout
            if (i+1) % 10 == 0:
                print(f"Processed {i+1}/{len(images)} images...")
            time.sleep(0.5)

    print("Synthesizing results into top 4 categories...")
    synthesis_prompt = f"""
    I have analyzed {len(images)} academic diagrams and extracted their layout structures.
    Here is the list of extracted layouts:
    {json.dumps(results, ensure_ascii=False)}
    
    Please cluster these completely into exactly FOUR distinct, highly representative causal mechanism layout categories.
    For each of the 4 categories, provide:
    1. A formal category name (e.g., "多层级纵向传导架构").
    2. A brief description of the visual layout and the causal logic it represents.
    3. Representative source image IDs.
    
    Output the 4 categories clearly numbered.
    """
    
    try:
        synth_response = client.models.generate_content(
            model='gemini-2.5-pro',
            contents=[synthesis_prompt]
        )
        
        output_path = os.path.join(os.path.dirname(__file__), "..", "references", "extracted_4_clusters.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(synth_response.text)
            
        print(f"Done! Saved clusters to {output_path}")
    except Exception as e:
        print(f"Error during synthesis: {e}")

if __name__ == "__main__":
    main()
