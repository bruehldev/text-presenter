import nltk
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


def generate_headline(text):
    tokenizer = AutoTokenizer.from_pretrained(
        "fabiochiu/t5-small-medium-title-generation"
    )
    model = AutoModelForSeq2SeqLM.from_pretrained(
        "fabiochiu/t5-small-medium-title-generation"
    )
    inputs = ["summarize: " + text]

    inputs = tokenizer(inputs, truncation=True, return_tensors="pt")
    output = model.generate(
        **inputs, num_beams=10, do_sample=True, min_length=5, max_length=32
    )
    decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
    predicted_title = nltk.sent_tokenize(decoded_output.strip())[0]

    return predicted_title
