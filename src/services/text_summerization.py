from transformers import pipeline

summarizer = pipeline("summarization", model="Falconsai/text_summarization")


def summarize(text, max_length=100, min_length=30, do_sample=True):
    text_length = len(text)
    if text_length < 100:
        max_length = text_length
        min_length = 40
    result = summarizer(
        text, max_length=max_length, min_length=min_length, do_sample=do_sample
    )
    summary_text = result[0]["summary_text"]
    return summary_text
