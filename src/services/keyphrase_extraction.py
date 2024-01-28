import numpy as np
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    TokenClassificationPipeline,
)
from transformers.pipelines import AggregationStrategy


# Define keyphrase extraction pipeline
class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])


def extract_keyphrases(text):
    # clean text
    text = text.replace("\n", " ")
    # Load pipeline
    model_name = "ml6team/keyphrase-extraction-kbir-inspec"
    extractor = KeyphraseExtractionPipeline(model=model_name)
    return extractor(text)
