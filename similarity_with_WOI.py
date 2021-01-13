import spacy

nlp = spacy.load('en_core_web_sm') # make sure to use larger model!

def findSimilarWOI(token1, token2):

    token1 = nlp(token1)
    token2 = nlp(token2)
    return token1.similarity(token2)