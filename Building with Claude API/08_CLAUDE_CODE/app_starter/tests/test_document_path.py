import os
import pytest
from tools.document import document_path_to_markdown


class TestDocumentPathToMarkdown:
    FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")
    DOCX_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.docx")
    PDF_FIXTURE = os.path.join(FIXTURES_DIR, "mcp_docs.pdf")

    # --- Happy path ---

    def test_pdf_returns_string(self):
        """Valid PDF path returns a str."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert isinstance(result, str)

    def test_pdf_returns_non_empty(self):
        """Valid PDF path returns non-empty content."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert len(result) > 0

    def test_docx_returns_string(self):
        """Valid DOCX path returns a str."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert isinstance(result, str)

    def test_docx_returns_non_empty(self):
        """Valid DOCX path returns non-empty content."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert len(result) > 0

    def test_pdf_content_fidelity(self):
        """Markdown output contains text that was in the original PDF."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        # The fixture is about MCP docs — check for a known term
        assert "MCP" in result or "Model Context Protocol" in result

    def test_docx_content_fidelity(self):
        """Markdown output contains text that was in the original DOCX."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert "MCP" in result or "Model Context Protocol" in result

    # --- File type inference ---

    def test_infers_pdf_extension(self):
        """Tool correctly handles a .pdf extension without being told explicitly."""
        result = document_path_to_markdown(self.PDF_FIXTURE)
        assert len(result) > 0

    def test_infers_docx_extension(self):
        """Tool correctly handles a .docx extension without being told explicitly."""
        result = document_path_to_markdown(self.DOCX_FIXTURE)
        assert len(result) > 0

    def test_case_insensitive_pdf_extension(self, tmp_path):
        """Uppercase .PDF extension is handled correctly."""
        upper_path = tmp_path / "mcp_docs.PDF"
        upper_path.write_bytes(open(self.PDF_FIXTURE, "rb").read())
        result = document_path_to_markdown(str(upper_path))
        assert isinstance(result, str)
        assert len(result) > 0

    def test_case_insensitive_docx_extension(self, tmp_path):
        """Mixed-case .Docx extension is handled correctly."""
        mixed_path = tmp_path / "mcp_docs.Docx"
        mixed_path.write_bytes(open(self.DOCX_FIXTURE, "rb").read())
        result = document_path_to_markdown(str(mixed_path))
        assert isinstance(result, str)
        assert len(result) > 0

    # --- Error handling ---

    def test_nonexistent_file_raises_error(self):
        """A path that does not exist raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            document_path_to_markdown("/tmp/does_not_exist_abc123.pdf")

    def test_directory_path_raises_error(self):
        """Passing a directory path instead of a file raises an error."""
        with pytest.raises((IsADirectoryError, ValueError, OSError)):
            document_path_to_markdown(self.FIXTURES_DIR)

    def test_unsupported_extension_raises_error(self, tmp_path):
        """An unsupported file extension raises a ValueError."""
        unsupported = tmp_path / "file.txt"
        unsupported.write_text("hello")
        with pytest.raises(ValueError):
            document_path_to_markdown(str(unsupported))

    def test_empty_file_raises_error(self, tmp_path):
        """An empty file raises an appropriate error."""
        empty = tmp_path / "empty.pdf"
        empty.write_bytes(b"")
        with pytest.raises(Exception):
            document_path_to_markdown(str(empty))
