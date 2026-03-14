# Document to Markdown Converter

A web application to convert various document formats to Markdown.

## Supported Formats

- Word documents (.docx, .doc)
- PDF files (.pdf)
- PowerPoint presentations (.pptx)
- Excel spreadsheets (.xlsx, .xls)
- HTML files (.html, .htm)
- EPUB books (.epub)
- OpenDocument text (.odt)
- Rich Text Format (.rtf)
- Images (.png, .jpg, .jpeg, .gif, .bmp)
- Audio files (.mp3, .wav)
- Video files (.mp4)

## Prerequisites

1. **Python 3.8+**

## Setup

### Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python main.py
```

The API will run on `http://localhost:8000`

### Frontend

Open `frontend/index.html` in your browser, or serve it:

```bash
cd frontend
python -m http.server 8080
```

Then visit `http://localhost:8080`

## API Endpoints

- `GET /` - API health check
- `POST /convert` - Convert a document
  - Form data: `file` (multipart/form-data)
  - Returns: JSON with markdown content and download URL

## Usage

1. Drag & drop or select a document
2. Wait for conversion
3. Preview the markdown or view raw output
4. Download the converted markdown file

## Libraries Used

### Backend
| Library | Version | Purpose |
|---|---|---|
| [FastAPI](https://fastapi.tiangolo.com/) | 0.104.1 | Web framework for the REST API |
| [Uvicorn](https://www.uvicorn.org/) | 0.24.0 | ASGI server to run FastAPI |
| [MarkItDown](https://github.com/microsoft/markitdown) | 0.0.1a3 | Microsoft library that converts documents, images, audio & video to Markdown |
| [python-multipart](https://github.com/Kludex/python-multipart) | 0.0.6 | Parses multipart file uploads |

### Frontend
| Library | Version | Purpose |
|---|---|---|
| [marked.js](https://marked.js.org/) | latest (CDN) | Renders raw Markdown as HTML for the live preview |

## Project Structure

```
mdconvert/
├── backend/
│   ├── main.py          # FastAPI application
│   └── requirements.txt # Python dependencies
├── frontend/
│   └── index.html       # Web interface
├── uploads/             # Temporary upload directory
└── output/              # Converted markdown files
```
