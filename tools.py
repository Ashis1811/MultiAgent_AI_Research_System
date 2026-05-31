from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
import io
from dotenv import load_dotenv
from rich import print
# import pytesseract
try:
    import pytesseract
except ModuleNotFoundError:
    pytesseract = None

from PIL import Image

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str, max_results: int = 10) -> str:
    """
    Search the web for recent and reliable information.

    Args:
        query: Search topic
        max_results: Number of search results to return
    """
    results = tavily.search(query=query, max_results=max_results)

    out = []

    for r in results['results']:

        out.append(
            f"""
            Title: {r['title']}
            URL: {r['url']}
            Snippet:
            {r['content'][:300]}
            ------------------------
            """
                    )

    return "\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""

    try:

        resp = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text[:5000]

    except Exception as e:

        return f"Could not scrape URL: {str(e)}"


# ─────────────────────────────────────────────────────────────
# PDF Extraction
# ─────────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using PyMuPDF."""

    try:

        try:
            try:
                import fitz  # PyMuPDF (import name provided by the pymupdf package)
            except Exception:  # pragma: no cover - optional dependency
                fitz = None
        except Exception:
            try:
                # Some environments may expose the module as PyMuPDF
                from PyMuPDF import fitz  # type: ignore
            except Exception:
                fitz = None

        doc = fitz.open(stream=file_bytes, filetype="pdf")

        text = ""

        for page in doc:

            text += page.get_text()

        text = text.strip()

        if not text:

            return "No readable text found in PDF."

        return text[:8000]

    except Exception as e:

        return f"Could not extract PDF text: {str(e)}"


# ─────────────────────────────────────────────────────────────
# IMAGE OCR Extraction
# ─────────────────────────────────────────────────────────────

def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from image using OCR."""

    try:

        # Windows Tesseract path
        pytesseract.pytesseract.tesseract_cmd = (
            r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )

        image = Image.open(io.BytesIO(file_bytes))

        # Improve OCR accuracy
        image = image.convert("L")

        # text = pytesseract.image_to_string(image)
       if pytesseract:
            text = pytesseract.image_to_string(image)
       else:
            text = "OCR unavailable in deployed environment."

        text = text.strip()

        if not text:

            return "No readable text detected in image."

        return text[:5000]

    except Exception as e:

        return f"Could not extract image text: {str(e)}"


# ─────────────────────────────────────────────────────────────
# TEXT FILE Extraction
# ─────────────────────────────────────────────────────────────

def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode plain text / markdown / csv files."""

    try:

        return file_bytes.decode(
            "utf-8",
            errors="replace"
        )[:8000]

    except Exception as e:

        return f"Could not read text file: {str(e)}"


# ─────────────────────────────────────────────────────────────
# MAIN FILE CONTENT EXTRACTOR
# ─────────────────────────────────────────────────────────────

def extract_file_content(uploaded_file) -> str:
    """
    Universal file parser for:
    PDF, Images, TXT, MD, CSV
    """

    try:

        file_bytes = uploaded_file.read()

        filename = uploaded_file.name.lower()

        # ── PDF ─────────────────────────

        if filename.endswith(".pdf"):

            return extract_text_from_pdf(file_bytes)

        # ── IMAGE FILES ─────────────────

        elif filename.endswith(
            (
                ".png",
                ".jpg",
                ".jpeg",
                ".webp",
                ".bmp",
                ".tiff"
            )
        ):

            return extract_text_from_image(file_bytes)

        # ── TEXT FILES ──────────────────

        elif filename.endswith(
            (
                ".txt",
                ".md",
                ".csv"
            )
        ):

            return extract_text_from_txt(file_bytes)

        # ── UNKNOWN FILE ────────────────

        else:

            return (
                "Unsupported file format.\n"
                "Supported: PDF, PNG, JPG, JPEG, WEBP, BMP, TIFF, TXT, MD, CSV"
            )

    except Exception as e:

        return f"File processing error: {str(e)}"
