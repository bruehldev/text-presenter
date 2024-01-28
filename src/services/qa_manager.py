from transformers import pipeline


def generate_answer(question, text, model_name):
    nlp = pipeline("question-answering", model=model_name, tokenizer=model_name)

    QA_input = {"question": question, "context": text}

    res = nlp(QA_input)

    return res["answer"]
