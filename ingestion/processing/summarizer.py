from transformers import pipeline, AutoTokenizer

MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

summarizer = pipeline("summarization", model=MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def summarize_text(text, max_input_tokens=1024):
    """
    Tronque proprement le texte à max_input_tokens avant résumé.
    """
    # Tokenisation
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=max_input_tokens)

    # Décodage tronqué pour le passage au modèle
    truncated_text = tokenizer.decode(inputs["input_ids"][0], skip_special_tokens=True)

    # Résumé
    summary = summarizer(
        truncated_text,
        max_length=180,
        min_length=50,
        do_sample=False
    )

    return summary[0]['summary_text']



# Tu peux remplacer le modèle par facebook/bart-large-cnn ou t5-small si besoin.
