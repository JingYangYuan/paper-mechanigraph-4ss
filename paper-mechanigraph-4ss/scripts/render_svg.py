import sys
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def svg_to_png(svg_path, png_path):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1800,1600")
    chrome_options.add_argument("--force-device-scale-factor=1")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        abs_path = os.path.abspath(svg_path)
        file_url = f"file:///{abs_path.replace(os.sep, '/')}"
        
        driver.get(file_url)
        time.sleep(0.5)
        
        # Target the exact SVG root element
        svg_element = driver.find_element("tag name", "svg")
        svg_element.screenshot(png_path)
        print(f"Successfully rendered {svg_path} to {png_path}")
    except Exception as e:
        print(f"Error rendering SVG: {e}")
        sys.exit(1)
    finally:
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python render_svg.py <input.svg> <output.png>")
        sys.exit(1)
    
    svg_to_png(sys.argv[1], sys.argv[2])
