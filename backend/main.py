from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from markitdown import MarkItDown
from pathlib import Path

app = FastAPI(title="Document to Markdown Converter")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
OUTPUT_DIR = Path(__file__).parent.parent / "output"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app.mount("/output", StaticFiles(directory=str(OUTPUT_DIR)), name="output")

md = MarkItDown()

SUPPORTED_EXTENSIONS = {
    ".docx", ".doc", ".pdf", ".pptx",
    ".html", ".htm", ".epub", ".odt", ".rtf",
    ".xlsx", ".xls", ".csv", ".png", ".jpg", ".jpeg", ".gif", ".bmp",
    ".mp3", ".wav", ".mp4", ".wav"
}


def convert_to_markdown(file_path: Path) -> str:
    result = md.convert(str(file_path))
    return result.text_content


@app.get("/")
async def root():
    return {"message": "Document to Markdown Converter API"}


@app.post("/convert")
async def convert_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")

    file_ext = Path(file.filename).suffix.lower()

    if file_ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_ext}. Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )

    file_path = UPLOAD_DIR / file.filename
    output_filename = Path(file.filename).stem + ".md"
    output_path = OUTPUT_DIR / output_filename

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        markdown = convert_to_markdown(file_path)
        output_path.write_text(markdown, encoding="utf-8")

        return JSONResponse(
            content={
                "success": True,
                "filename": output_filename,
                "download_url": f"/output/{output_filename}",
                "markdown": markdown
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if file_path.exists():
            file_path.unlink()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
