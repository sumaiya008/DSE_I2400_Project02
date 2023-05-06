
sentences = [
    "blood cancer","cancer"
]

from sentence_transformers import SentenceTransformer

model = SentenceTransformer('bert-base-nli-mean-tokens')


sentence_embeddings = model.encode(sentences)

print(sentence_embeddings.shape)

from sklearn.metrics.pairwise import cosine_similarity

print(cosine_similarity(
    [sentence_embeddings[0]],
    sentence_embeddings[1:]
))



# for i in range(len(d1)):
#
#
# { {'keyword': "cancer", "url": "avsbc@bshdf" ,'text':'hgowehrijoirjwpepojopfe'},
#
#
#
#   {'keyword': "cancer", "url": "avsbc@bshdf" ,'text':'hgowehrijoirjwpepojopfe'}}
