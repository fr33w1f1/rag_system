# core/processing/pdf_processor.py
import pymupdf4llm
import uuid
from typing import List, Dict
from langchain.schema import Document
from core.processing.document_splitter import HierarchyMarkdownHeaderTextSplitter

class PDFProcessor:
    @staticmethod
    def split(pdf_path: str) -> List[Document]:
        """Split chunks larger than max_chunk_size using header hierarchy"""
        splitter = HierarchyMarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3")
            ],
            strip_headers=True
        )
        markdown_text = pymupdf4llm.to_markdown(
            doc=pdf_path,
        )
        documents = splitter.split_text(markdown_text)

        for doc in documents:
            doc.metadata["source"] = pdf_path

        return documents
    
if __name__ == "__main__":
    chunk = PDFProcessor.split('notebooks/2408-09869v5.pdf')
    print(chunk[0])