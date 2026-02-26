from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    path: str = Field(description="Absolute or relative path to a PDF or DOCX file"),
) -> str:
    """Convert a PDF or DOCX file on disk to markdown-formatted text.

    Reads the file at the given path, detects the file type from its extension,
    and returns the document contents as markdown.

    When to use:
    - When you have a local file path to a PDF or DOCX document
    - When you need the text content of a document as markdown

    Examples:
    >>> document_path_to_markdown("/tmp/report.pdf")
    "# Report\\n\\nContents..."
    """
    p = Path(path)

    if not p.exists():
        raise FileNotFoundError(f"No file found at path: {path}")

    if not p.is_file():
        raise IsADirectoryError(f"Path is not a file: {path}")

    ext = p.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file extension '{p.suffix}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )

    binary_data = p.read_bytes()
    return binary_document_to_markdown(binary_data, ext.lstrip("."))
