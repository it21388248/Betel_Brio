from pdfminer.high_level import extract_text as extract_pdf
from docx import Document

def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            print("📄 Extracting text from PDF...")
            return extract_pdf(file_path)

        elif file_path.endswith(".docx"):
            print("📄 Extracting text from DOCX...")
            doc = Document(file_path)
            return "\n".join(p.text for p in doc.paragraphs)

        elif file_path.endswith((".txt", ".csv", ".xml")):
            print("📄 Extracting text from Plain file...")
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        else:
            print(f"⚠️ Unsupported file type: {file_path}")
            return None

    except Exception as e:
        print(f"❌ Error extracting text from file '{file_path}':", str(e))
        return None
