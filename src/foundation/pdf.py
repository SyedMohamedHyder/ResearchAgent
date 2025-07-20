import fitz

def read_pdf(file_path: str) -> str:
    """
    Extracts and returns all text from a PDF file using PyMuPDF.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Complete extracted text from the PDF.
    """
    try:
        with fitz.open(file_path) as doc:
            text_pages = [page.get_text("text").strip() for page in doc]
        return "\n\n".join(text_pages)
    except Exception as e:
        raise RuntimeError(f"Error reading PDF '{file_path}': {e}")
