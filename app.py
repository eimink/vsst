#!/usr/bin/env python3
"""
Slideshow server: serves images and websites from a content folder
"""

import os
import json
from pathlib import Path
from flask import Flask, render_template, jsonify, send_file

app = Flask(__name__)

# Content folder path
CONTENT_DIR = Path("/content")
SLIDE_DURATION = 10  # seconds per slide (configurable via environment if needed)

# Supported image extensions
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.svg'}


def get_slides():
    """Scan content folder and return sorted list of slides (images and .url files)"""
    if not CONTENT_DIR.exists():
        return []
    
    slides = []
    
    # Scan for images and .url files
    for item in sorted(CONTENT_DIR.iterdir()):
        if item.is_file():
            if item.suffix.lower() in IMAGE_EXTENSIONS:
                slides.append({
                    'type': 'image',
                    'name': item.name,
                    'src': f'/media/{item.name}'
                })
            elif item.suffix.lower() == '.url':
                # Read URL from file
                try:
                    with open(item, 'r') as f:
                        url = f.read().strip()
                    if url:
                        slides.append({
                            'type': 'iframe',
                            'name': item.name,
                            'src': url
                        })
                except Exception as e:
                    print(f"Error reading {item.name}: {e}")
    
    return slides


@app.route('/')
def index():
    """Serve the slideshow page"""
    return render_template('index.html', slide_duration=SLIDE_DURATION)


@app.route('/api/slides')
def api_slides():
    """API endpoint returning list of slides"""
    slides = get_slides()
    return jsonify({
        'slides': slides,
        'duration': SLIDE_DURATION
    })


@app.route('/media/<path:filename>')
def serve_media(filename):
    """Serve media files from content folder"""
    file_path = CONTENT_DIR / filename
    
    # Security: ensure file is within CONTENT_DIR
    try:
        file_path.resolve().relative_to(CONTENT_DIR.resolve())
    except ValueError:
        return "Forbidden", 403
    
    if not file_path.exists() or not file_path.is_file():
        return "Not Found", 404
    
    return send_file(file_path)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
