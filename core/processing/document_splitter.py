from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain.schema import Document

class HierarchyMarkdownHeaderTextSplitter(MarkdownHeaderTextSplitter):
    def split_text(self, text: str) -> list[Document]:
        splits = super().split_text(text)
        for doc in splits:
            headers = " > ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
            doc.page_content = f"{headers}\n\n{doc.page_content}"
        return splits   