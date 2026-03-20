import streamlit as st
import spacy
import pdfplumber
from docx import Document

nlp = spacy.load("en_core_web_sm")

st.title("?? Smart Study Assistant (NER Chatbot)")

uploaded_file = st.file_uploader("Upload PDF or Word file", type=["pdf", "docx"])

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

if uploaded_file:
    text = extract_text(uploaded_file)

    st.subheader("?? Extracted Text")
    st.write(text[:1000])  # preview

    doc = nlp(text)

    st.subheader("?? Named Entities")
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    for ent in entities:
        st.write(f"{ent[0]} ? {ent[1]}")