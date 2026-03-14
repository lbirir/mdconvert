# Development Guidelines

## Build & Run Commands

### Backend (Python/FastAPI)

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (macOS/Linux)
source venv/bin/activate

# Activate virtual environment (Windows)
# venv\Scripts\activate

# Start the server
python main.py

# Or using uvicorn directly
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend

```bash
# Serve with Python
cd frontend
python -m http.server 8080

# Or simply open index.html in browser
```

### Testing

Currently no test framework is installed.

To add tests, install pytest:
```bash
cd backend
source venv/bin/activate
pip install pytest pytest-asyncio httpx
pytest              # Run all tests
pytest test_main.py # Run specific test file
```

## Python Code Style

### Imports
- Follow standard library order: stdlib → third-party → local imports
- Use `from module import Class` for specific classes
- Use `import module` for modules with many exports
- Keep imports at file top with one blank line after

### Naming Conventions
- **Files**: lowercase with underscores (main.py)
- **Functions**: snake_case (convert_docx_to_markdown)
- **Classes**: PascalCase (FastAPI, Presentation)
- **Constants**: SCREAMING_SNAKE_CASE (UPLOAD_DIR, OUTPUT_DIR)
- **Variables**: snake_case (file_path, markdown_content)

### Types
- Use type hints for all function arguments
- Use type hints for return values
- Use `Optional` for nullable returns
- Use `Path` from pathlib for file paths instead of strings

### Error Handling
- Use `HTTPException` for API errors with `status_code` and `detail`
- Use `try/except/finally` for file operations
- Use `subprocess.CalledProcessError` for external command failures
- Use `FileNotFoundError` when files are missing
- Clean up temp files in `finally` blocks

### Path Handling
- Use `pathlib.Path` exclusively, not `os.path`
- Access parent with `.parent`
- Get suffix with `.suffix`
- Read file with `.read_text(encoding="utf-8")`
- Write file with `.write_text(text, encoding="utf-8")`
- Check existence with `.exists()`
- Delete file with `.unlink()`

### Function Design
- One function per conversion type
- Return strings, don't print
- Accept `Path` objects, not strings
- Use descriptive names: `convert_X_to_markdown`

### Async Code
- Use `async`/`await` for I/O operations
- Use `async with` for async context managers
- Use `UploadFile` from FastAPI for file uploads

## FastAPI Patterns

### Endpoint Definition
```python
@app.get("/")
async def root() -> dict:
    return {"message": "Health check"}

@app.post("/convert")
async def convert_document(file: UploadFile = File(...)) -> JSONResponse:
    # Use File(...) default for required uploads
    # Return JSONResponse for structured responses
```

### CORS Middleware
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Customize for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Response Types
- Use `JSONResponse` for structured data
- Use `FileResponse` for file downloads
- Use `StaticFiles` for serving static directories

## Dependencies (backend/requirements.txt)

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `python-multipart` - Form data parsing
- `mammoth` - DOCX conversion
- `pdfplumber` - PDF text extraction
- `python-pptx` - PPTX handling
- `html2text` - HTML to markdown
- `pandoc` - Multi-format conversion

Always verify new dependencies match existing versions for type and return value style.

## External Tools Required

### Pandoc (multi-format conversion)
```bash
# macOS
brew install pandoc

# Verify installation
pandoc --version
```

## Git Workflow

```bash
# Stage changes
git add .

# Commit with conventional commits
git commit -m "feat: add EPUB support"
git commit -m "fix: handle empty PDF pages"
git commit -m "refactor: extract PDF extraction to function"

# Push
git push
```

## Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use breakpoints
breakpoint()

# Type checking
mypy main.py
```

## File Cleanup

Always remove uploaded files after processing:
```python
try:
    # processing logic
finally:
    if file_path.exists():
        file_path.unlink()
```

## Security Notes

- Validate file extensions before processing
- Sanitize filenames to prevent path traversal
- Use `Path().resolve()` for absolute paths
- Limit allowed MIME types if needed in production
