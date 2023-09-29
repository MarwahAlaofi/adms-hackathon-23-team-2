import pandas as pd
import nltk
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import word_tokenize
from scipy.stats import entropy
import matplotlib.pyplot as plt

stopwords_ext = [
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
    "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
    "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
    "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
    "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
    "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
    "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
    "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
    "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
    "they've", "this", "those", "through", "to", "too", "under", "until", "up",
    "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
    "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
    "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
    "yourself", "yourselves", "may", "also", "yes", "rather", "might", "within", "http", "https"
]
# Custom stopwords
custom_stopwords = list(nltk.corpus.stopwords.words('english')) +stopwords_ext

# Read the CSV file and preprocess data
file_path = '../data/V1-during-hackathon/model_votes_campaign_given_persona.csv'
data = pd.read_csv(file_path)
data['answer'].fillna("", inplace=True)

# Initialize stemmer and a dictionary to map stemmed words to their original form
stemmer = SnowballStemmer("english")
stem_to_original = {}


def tokenize_and_stem(text):
    text = re.sub(r'[\u00B0-\u00B9\u00B2-\u00B3\u2070-\u209F]+', '', text.lower())
    tokens = [word for word in word_tokenize(text) if re.match(r'[A-Za-z]+', word) and word not in custom_stopwords]
    stemmed_tokens = [stemmer.stem(t) for t in tokens]
    stem_to_original.update({stemmed: orig for stemmed, orig in zip(stemmed_tokens, tokens)})
    return stemmed_tokens


# Count Vectorizer setup
count_vectorizer = CountVectorizer(tokenizer=tokenize_and_stem, stop_words=custom_stopwords)
count_matrix = count_vectorizer.fit_transform(data['answer']).toarray()
word_probs = count_matrix.sum(axis=0) / count_matrix.sum()

# TF-IDF Vectorizer setup
tfidf_vectorizer = TfidfVectorizer(tokenizer=tokenize_and_stem, stop_words=custom_stopwords)
tfidf_matrix = tfidf_vectorizer.fit_transform(data['answer']).toarray()


def kl_divergence(doc_freqs):
    doc_probs = doc_freqs / (doc_freqs.sum() or 1)
    return entropy([doc_probs, word_probs], base=2)


results_list = []

for i, doc in enumerate(data['answer']):
    row_data = data.loc[i, ['model', 'persona', 'type']]

    # Jaccard distinct words
    words_in_doc = set(tokenize_and_stem(doc))
    words_in_other_docs = set(tokenize_and_stem(" ".join(data['answer'].drop(i))))
    dis_words = [stem_to_original[word] for word in words_in_doc - words_in_other_docs]

    # KL Divergence
    kl_words = [stem_to_original[word] for word in
                count_vectorizer.get_feature_names_out()[kl_divergence(count_matrix[i]).argsort()[-10:]]]

    # TF-IDF
    tfidf_words = [stem_to_original[word] for word in
                   tfidf_vectorizer.get_feature_names_out()[tfidf_matrix[i].argsort()[-10:]]]

    results_list.append({
        'Model': row_data['model'],
        'Persona': row_data['persona'],
        'Type': row_data['type'],
        'Distinct Words': ', '.join(dis_words),
        'Top KL Divergent Words': ', '.join(kl_words),
        'Top TF-IDF Words': ', '.join(tfidf_words)
    })

results_df = pd.DataFrame(results_list)
results_df.to_csv("../results/dist_words_model_persona.csv")
print(results_df.to_markdown())

