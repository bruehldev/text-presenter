import re
from transformers import AutoTokenizer, T5ForConditionalGeneration


def generate_headline(text):
    WHITESPACE_HANDLER = lambda k: re.sub("\s+", " ", re.sub("\n+", " ", k.strip()))
    model_name = "JulesBelveze/t5-small-headline-generator"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    input_ids = tokenizer(
        [WHITESPACE_HANDLER(text)],
        return_tensors="pt",
        padding="max_length",
        truncation=True,
        max_length=384,
    )["input_ids"]
    output_ids = model.generate(
        input_ids=input_ids, max_length=84, no_repeat_ngram_size=2, num_beams=4
    )[0]
    summary = tokenizer.decode(
        output_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False
    )
    return summary
