from transformers import BertTokenizer, BertModel
import torch
import umap
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import HDBSCAN
import threading


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")
model = model.to(device)


def get_words_and_embeddings(text):
    # Tokenize the text
    tokens = tokenizer(text, truncation=True, return_tensors="pt", max_length=512)

    # Split the input into chunks of 512 tokens or less
    input_ids_chunks = tokens["input_ids"].split(512)

    # Initialize an empty list to store the embeddings
    all_embeddings = []

    for input_ids in input_ids_chunks:
        input_ids = input_ids.to(device)

        # Get BERT embeddings
        with torch.no_grad():
            outputs = model(input_ids)
            hidden_states = outputs[0]
            first_token_embeddings = hidden_states[0]

        # Reduce embeddings to 2 dimensions using UMAP
        reducer = umap.UMAP(
            metric="cosine", n_components=2, random_state=42, n_neighbors=5
        )
        first_token_embeddings_cpu = first_token_embeddings.cpu()
        reduced_embeddings = reducer.fit_transform(first_token_embeddings_cpu)

        # Aggregate subword embeddings to obtain word embeddings
        word_to_embedding = {}
        current_word = ""
        current_position = []

        for i, (word_id, embedding) in enumerate(zip(input_ids[0], reduced_embeddings)):
            # skip first and last token
            if i in [0, len(input_ids[0]) - 1]:
                continue

            word = tokenizer.convert_ids_to_tokens([word_id])[0]
            if "##" in word:
                current_word += word.replace("##", "")
                current_position.append(embedding)
            else:
                if current_word:  # Only aggregate when current_word is not empty
                    aggregated_embedding = np.mean(current_position, axis=0)
                    word_to_embedding[current_word] = aggregated_embedding
                current_word = word  # Start a new word
                current_position = [embedding]  # Start a new position list

        # aggregate the last word
        if current_word:
            aggregated_embedding = np.mean(current_position, axis=0)
            word_to_embedding[current_word] = aggregated_embedding

    return word_to_embedding


def get_cluster_labels(word_to_embedding):
    # Cluster word_to_embedding using HDBSCAN
    clusterer = HDBSCAN(
        min_cluster_size=10, metric="euclidean", cluster_selection_method="eom"
    )
    cluster_labels = clusterer.fit_predict(list(word_to_embedding.values()))
    return cluster_labels


def plot_embeddings(word_to_embedding, cluster_labels):
    # Plot the embeddings from word_to_embedding and color them by cluster
    plt.scatter(
        [emb[0] for emb in word_to_embedding.values()],
        [emb[1] for emb in word_to_embedding.values()],
        c=cluster_labels,
    )

    # Annotate the plot with the words
    for i, word in enumerate(word_to_embedding.keys()):
        plt.annotate(word, list(word_to_embedding.values())[i])

    plt.show()


def start_plot(text):
    word_to_embedding = get_words_and_embeddings(text)
    cluster_labels = get_cluster_labels(word_to_embedding)
    plot_embeddings(word_to_embedding, cluster_labels)
