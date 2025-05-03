# core/processing/pdf_processor.py
import pymupdf4llm
import uuid
from typing import List, Dict
from core.processing.document_splitter import HierarchyMarkdownHeaderTextSplitter

class PDFProcessor:
    @staticmethod
    def pdf_to_markdown(pdf_path: str) -> str:
        """Convert PDF to structured Markdown chunks with metadata"""
        markdown_format = pymupdf4llm.to_markdown(
            doc=pdf_path,
        )
        return markdown_format
    
    @staticmethod
    def split_markdown_chunks(markdown: List[Dict]) -> List[Dict]:
        """Split chunks larger than max_chunk_size using header hierarchy"""
        splitter = HierarchyMarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3")
            ],
            strip_headers=True
        )
        md_header_splits = splitter.split_text(markdown)

        return md_header_splits
    
if __name__ == "__main__":
    doc = PDFProcessor.pdf_to_markdown('notebooks/2408-09869v5.pdf')
    chunk = PDFProcessor.split_markdown_chunks(doc)
    print(chunk[3])