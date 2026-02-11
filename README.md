# Very Simple Slideshow Tunkki - Slideshow Kiosk

A lightweight, containerized slideshow system for displaying images and web content in fullscreen mode. Perfect for kiosks, displays, and presentations.

## Features

- **Fullscreen Slideshow**: Auto-rotating slides with fixed duration per slide
- **Image Support**: JPG, PNG, GIF, SVG images
- **Web Content**: Display websites/web pages as fullscreen iframes
- **Responsive Design**: Supports both 16:9 and 9:16 aspect ratios
- **Local Deployment**: Runs entirely locally without internet connection
- **Zero Configuration**: Just point to a folder and run
- **Dockerized**: Easy deployment and consistency across machines

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- A folder with images and/or `.url` files

### Installation & Running

1. **Clone the repository**
   ```bash
   git clone git@github.com:eimink/vsst.git
   cd vsst
   ```

2. **Add content to the `content/` folder**
   - Place images (`.jpg`, `.png`, `.gif`, `.svg`) directly in the folder
   - Create `.url` files with a single URL per file for web content
   - Files are displayed in alphabetical order

3. **Start the slideshow**
   ```bash
   docker compose up --build
   ```

4. **Access the slideshow**
   - Open in browser: `http://localhost:5000`
   - Or from another machine: `http://<your-machine-ip>:5000`

## Content Structure

```
content/
├── 01_image.jpg
├── 02_image.png
└── 03_website.url    # Contains single URL like: http://localhost:8080
```

### Creating URL files

Create a `.url` file with the URL of the content you want to display:

```bash
echo "http://myservice:8080" > content/my_website.url
```

## Configuration

Edit `app.py` to change:
- `SLIDE_DURATION`: Duration per slide in seconds (default: 5)
- `CONTENT_DIR`: Content folder path (default: `/content`)
- `IMAGE_EXTENSIONS`: Supported image formats

## Multi-Container Setup

To display content from another container, use Docker Compose networking:

```yaml
services:
  slideshow:
    # ... existing config
  
  my-website:
    image: my-web-app
    networks:
      - slideshow-network

networks:
  slideshow-network:
    driver: bridge
```

Then reference it in a `.url` file:
```bash
echo "http://my-website:8080" > content/my_site.url
```

## Project Structure

```
.
├── app.py                   # Flask backend
├── templates/
│   └── index.html          # Frontend (pure JS, no frameworks)
├── Dockerfile              # Container definition
├── docker-compose.yml      # Container orchestration
├── content/                # Media files (mount point)
└── README.md               # This file
```

## How It Works

1. **Backend** (`app.py`): 
   - Scans `/content` folder for images and `.url` files
   - Serves them via API endpoint (`/api/slides`)
   - Streams media files via `/media/<filename>`

2. **Frontend** (`index.html`):
   - Fetches slide list from API
   - Renders images as `<img>` tags
   - Renders URLs as fullscreen `<iframe>` elements
   - Auto-rotates with configurable duration

## Minimal Dependencies

- Python 3.11+
- Flask (only external dependency)
- No frontend frameworks or build tools required

## License

MIT
