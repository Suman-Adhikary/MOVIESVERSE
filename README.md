# MOVIE RECOMMENDED SYSTEM

A movie recommendation system employs advanced algorithms to analyze user preferences and viewing history, providing personalized film suggestions. By utilizing machine learning, it constantly refines its recommendations based on user feedback, enhancing accuracy over time. These systems often consider various factors, such as genre, director, and user ratings, to tailor suggestions to individual tastes. With the rise of streaming platforms, movie recommendation systems play a crucial role in helping users discover content that aligns with their interests, creating a more satisfying and immersive viewing experience. Ultimately, these systems bridge the gap between users and a vast array of films, making the selection process more seamless and enjoyable.



![App Screenshot](https://miro.medium.com/v2/resize:fit:2000/format:webp/1*rCK9VjrPgpHUvSNYw7qcuQ@2x.png)


## Deployment

To deploy this project install this modules.

```bash
  pip install numpy
  pip install pandas
  pip install sklearn
```


## Documentation

[Pandas](https://pandas.pydata.org/)
[Numpy](https://numpy.org/)
[sklearn](https://scikit-learn.org/stable/)

TF-IDF, or Term Frequency-Inverse Document Frequency, is a numerical statistic used in information retrieval and text mining. It quantifies the importance of a word in a document relative to a collection of documents, taking into account both the frequency of the term in the document and its rarity across the entire collection.

Term Frequency (TF): Measures how often a term appears in a document. The more frequent the term, the higher the TF value.

Inverse Document Frequency (IDF): Evaluates the rarity of a term across a collection of documents. If a term is rare and occurs in fewer documents, it receives a higher IDF score.

TF-IDF Score: Obtained by multiplying the TF and IDF values. A high TF-IDF score indicates that a term is both frequent in a particular document and rare in the entire collection, suggesting its significance in that document.

TF-IDF is widely used in natural language processing, information retrieval, and document analysis to extract key terms, identify important words, and rank documents based on their relevance to a given query. It helps in representing the content of documents in a numerical form, facilitating effective document similarity and relevance ranking.

![App Screenshot](https://www.kdnuggets.com/wp-content/uploads/awan_convert_text_documents_tfidf_matrix_tfidfvectorizer_3.png)

Cosine Similarity : The cosine similarity between two TF-IDF vectors (representing two documents) is computed by taking the dot product of the vectors and dividing it by the product of their magnitudes. This yields a value between -1 and 1.

A cosine similarity of 1 indicates perfect similarity.
A cosine similarity of 0 means no similarity.
A cosine similarity of -1 implies dissimilarity.

![App Screenshot](https://miro.medium.com/v2/resize:fit:720/format:webp/1*dyH20eCqb6qTL-gt4nCVzQ.png)
## Demo

https://moviesverse.streamlit.app/
