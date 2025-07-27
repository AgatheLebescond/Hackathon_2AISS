import spacy

nlp = spacy.load("en_core_web_sm")

def split_text_spacy(text, max_tokens=300):
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    chunks = []
    current_chunk = ""
    current_len = 0

    for sent in sentences:
        sent_len = len(sent.split())

        if current_len + sent_len <= max_tokens:
            current_chunk += " " + sent
            current_len += sent_len
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sent
            current_len = sent_len

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
