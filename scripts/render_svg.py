#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SVG to PNG Headless Renderer
Converts academic SVG diagrams to PNG using Selenium or native Headless Chrome CLI.
Provides cross-platform support (macOS, Linux, Windows) with graceful fallbacks.
"""

import sys
import os
import re
import shutil
import subprocess

def find_chrome_binary():
    """Locate Google Chrome or Chromium executable across OS platforms."""
    # 1. Check environment variable override
    env_chrome = os.environ.get("CHROME_BIN") or os.environ.get("GOOGLE_CHROME_BIN")
    if env_chrome and os.path.isfile(env_chrome) and os.access(env_chrome, os.X_OK):
        return env_chrome

    # 2. Check system PATH
    for name in ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"]:
        bin_path = shutil.which(name)
        if bin_path:
            return bin_path

    # 3. Platform specific locations
    if sys.platform == "darwin":
        mac_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
            os.path.expanduser("~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        ]
        for p in mac_paths:
            if os.path.exists(p):
                return p
    elif sys.platform.startswith("win"):
        win_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
        local_app = os.environ.get("LOCALAPPDATA")
        if local_app:
            win_paths.append(os.path.join(local_app, r"Google\Chrome\Application\chrome.exe"))
        for p in win_paths:
            if os.path.exists(p):
                return p
    elif sys.platform.startswith("linux"):
        linux_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ]
        for p in linux_paths:
            if os.path.exists(p):
                return p

    return None

def parse_svg_dimensions(svg_path):
    """Extract width and height from SVG viewBox or width/height attributes."""
    try:
        with open(svg_path, "r", encoding="utf-8") as f:
            content = f.read(2048)  # header chunk
        # Check viewBox="0 0 W H"
        vb = re.search(r'viewBox=["\']\s*[\d.]+\s+[\d.]+\s+([\d.]+)\s+([\d.]+)\s*["\']', content)
        if vb:
            return int(float(vb.group(1))), int(float(vb.group(2)))
        # Check width="W" height="H"
        w = re.search(r'width=["\']([\d.]+)p?x?["\']', content)
        h = re.search(r'height=["\']([\d.]+)p?x?["\']', content)
        if w and h:
            return int(float(w.group(1))), int(float(h.group(2)))
    except Exception:
        pass
    return 1200, 800

def render_with_chrome_cli(chrome_bin, svg_path, png_path, width, height):
    """Render using native headless Chrome CLI screenshot."""
    abs_svg = os.path.abspath(svg_path)
    abs_png = os.path.abspath(png_path)
    file_url = f"file:///{abs_svg.replace(os.sep, '/')}"

    cmd = [
        chrome_bin,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={width},{height}",
        f"--screenshot={abs_png}",
        file_url,
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
    if os.path.exists(abs_png) and os.path.getsize(abs_png) > 0:
        return True, f"Rendered via Chrome CLI ({width}x{height})"
    # Fallback to legacy headless if --headless=new failed
    cmd[1] = "--headless"
    res2 = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30)
    if os.path.exists(abs_png) and os.path.getsize(abs_png) > 0:
        return True, f"Rendered via Chrome CLI (legacy headless, {width}x{height})"
    return False, f"Chrome CLI screenshot failed: {res.stderr or res2.stderr}"

def render_with_selenium(svg_path, png_path, width, height):
    """Render using Selenium webdriver."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
    except ImportError:
        return False, "Selenium is not installed (run `pip install selenium`)"

    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument(f"--window-size={width},{height}")
        chrome_options.add_argument("--force-device-scale-factor=1")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--hide-scrollbars")

        chrome_bin = find_chrome_binary()
        if chrome_bin:
            chrome_options.binary_location = chrome_bin

        driver = webdriver.Chrome(options=chrome_options)
        try:
            abs_path = os.path.abspath(svg_path)
            file_url = f"file:///{abs_path.replace(os.sep, '/')}"
            driver.get(file_url)
            import time
            time.sleep(0.5)
            svg_element = driver.find_element("tag name", "svg")
            svg_element.screenshot(png_path)
            return True, f"Rendered via Selenium ({width}x{height})"
        finally:
            driver.quit()
    except Exception as e:
        return False, f"Selenium rendering failed: {e}"

def svg_to_png(svg_path, png_path):
    if not os.path.exists(svg_path):
        print(f"Error: Input SVG file does not exist: {svg_path}")
        sys.exit(1)

    width, height = parse_svg_dimensions(svg_path)

    # 1. Try native Chrome CLI (zero-dependency, fast, robust)
    chrome_bin = find_chrome_binary()
    if chrome_bin:
        ok, msg = render_with_chrome_cli(chrome_bin, svg_path, png_path, width, height)
        if ok:
            print(f"Successfully rendered {svg_path} -> {png_path} [{msg}]")
            return

    # 2. Try Selenium
    ok, msg = render_with_selenium(svg_path, png_path, width, height)
    if ok:
        print(f"Successfully rendered {svg_path} -> {png_path} [{msg}]")
        return

    # 3. Graceful degradation report
    print("\n" + "=" * 60)
    print("Warning: Visual rendering from SVG to PNG requires Chrome or Selenium.")
    print(f"- Target SVG was successfully preserved at: {os.path.abspath(svg_path)}")
    print("- To enable headless PNG rendering and automatic visual verification:")
    print("    1) Ensure Google Chrome or Chromium is installed.")
    print("    2) (Optional) Run: pip install selenium webdriver-manager")
    print("    3) Set CHROME_BIN environment variable if Chrome is in a custom path.")
    print("=" * 60 + "\n")
    # Exit with code 2 to indicate soft dependency warning without breaking file generation
    sys.exit(2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render_svg.py <input.svg> <output.png>")
        sys.exit(1)
    svg_to_png(sys.argv[1], sys.argv[2])
