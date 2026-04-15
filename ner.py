import streamlit as st
import spacy
import pdfplumber
from docx import Document
from spacy import displacy
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="Smart Study Assistant",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS for better look
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #f8fafc, #e2e8f0);
}

h1 {
    text-align: center;
    color: #1e3a8a;
    font-weight: bold;
}

h2, h3 {
    color: #0f172a;
}

div[data-testid="stFileUploader"] {
    background-color: white;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #dbeafe;
}

.stAlert {
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Title
st.markdown("<h1>🎓 Smart Study Assistant</h1>", unsafe_allow_html=True)
st.caption("AI Powered PDF & Word Document Analyzer")

# File uploader
uploaded_file = st.file_uploader(
    "📂 Upload PDF or Word file",
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

    if text is None or text.strip() == "":
        st.error("Unable to extract text from this file ❌")

    else:
        # Preview section
        st.subheader("📄 Extracted Text Preview")
        st.text_area("Document Content", text[:1000], height=250)

        st.markdown("---")

        # Limit text for processing
        processed_text = text[:2000]

        # NLP processing
        doc = nlp(processed_text)

        # Named entities
        st.subheader("🔍 Named Entities Recognition")

        if not doc.ents:
            st.warning("No entities found.")

        else:
            html = displacy.render(doc, style="ent", jupyter=False)
            components.html(html, height=500, scrolling=True)
