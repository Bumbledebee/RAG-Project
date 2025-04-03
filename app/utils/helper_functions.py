import fitz
import re

def say_hi():
    print("hi")

# load pdf
def load_pdf(file_path):
    content = []
    with fitz.open(file_path) as pdf:
        for page in pdf:
            content.append(page.get_text())
    return content

def clean_pdf(pages):
    cleaned_content = []
    for page in pages:
        # Remove excessive whitespace and possible document-related metadata
        text = re.sub(r'\s+', ' ', page)
        text = re.sub(r'^\d+\s+', '', text)  # Remove page numbers at the beginning

        # Remove the specific URLs and any preceding numbers like '1.1.3'
        text = re.sub(r'\b\d+\.\d+\.\d+\s+https://stats\.libretexts\.org/@go/page/\d+\b\s*', '', text)
        text = re.sub(r'https://stats\.libretexts\.org/@go/page/\d+\b\s*', '', text)

        # Remove BOM-like characters and any other non-ASCII characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)

        cleaned_content.append(text)
    return cleaned_content


def _get_document_prompt(docs):
    prompt = "\n"
    for doc in docs:
        prompt += "\nContent:\n"
        prompt += doc.page_content + "\n\n"
    return prompt
