import streamlit as st
import spacy
import pdfplumber
from docx import Document
from spacy import displacy
import streamlit.components.v1 as components

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# App title
st.title("📚 Smart Study Assistant (NER Chatbot)")

# File uploader
uploaded_file = st.file_uploader(
    "Upload PDF or Word file",
    type=["pdf", "docx"]
)

# Function to extract text
def extract_text(file):
    if file.type == "application/pdf":
        text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    else:
        return None


# Main logic
if uploaded_file is None:
    st.info("Please upload a PDF or Word file to begin.")

else:
    text = extract_text(uploaded_file)

    # Handle unsupported or empty text
    if text is None or text.strip() == "":
        st.error("Unable to extract text from this file ❌")

    else:
        # Show extracted text preview
        st.subheader("📄 Extracted Text (Preview)")
        st.write(text[:1000])

        # Limit text for performance (optional but recommended)
        processed_text = text[:2000]

        # Process NLP
        doc = nlp(processed_text)

        # Highlighted NER output
        st.subheader("🔍 Named Entities")

        if not doc.ents:
            st.warning("No entities found.")
        else:
            html = displacy.render(doc, style="ent", jupyter=False)
            components.html(html, height=500, scrolling=True)
