import spacy
nlp = spacy.load('en_core_web_sm')
from similarity_with_WOI import findSimilarWOI


def textCleaning(user_text):
    user_text = user_text.strip()
    return user_text

def sentenceTokenizer(user_text_clean):
    #  "nlp" Object is used to create documents with linguistic annotations.
    doc = nlp(user_text_clean)

    # create list of sentence tokens
    sents_list = []
    for sent in doc.sents:
        sents_list.append(sent.text)
    return sents_list

def wordTokenization(user_text_sents):
    doc = nlp(user_text_sents)

    # Create list of word tokens
    token_list = []
    for token in doc:
        if token.pos_ in ['PROPN', 'NOUN']:
            token_list.append(token.text)
    return token_list

def findMaxSimilarity(similarity):
    similarity = similarity[0]
    sorted_key_list = sorted(similarity, key=similarity.get, reverse=True)
    top_key_list = sorted_key_list[0]
    if len(top_key_list):
        return top_key_list
    else:
        return sorted_key_list

def printHeirarchy():
    pass

def findWOI(user_text, svos):
    # check if subject or object contains any words of interest
    # words of interest (list of all the words of interest as well as related words)
    # if yes, find head word of interest
    head_words_of_interest = ['car', 'automobile', 'four wheeler', 'sports', 'fitness', 'gym', 'food', 'pets', 'game', 'tech', 'books']
    similarity = []

    user_text_clean = textCleaning(user_text)
    user_text_sents = sentenceTokenizer(user_text_clean)
    for sentence in user_text_sents:
        tokens = wordTokenization(sentence)
        for token in tokens:
            for woi in head_words_of_interest:
                similarity_index = findSimilarWOI(token, woi)
                if similarity_index:
                    similarity.append({'sentence': sentence, 'token': token, 'WOI': woi, 'similarity': similarity_index})


    if len(similarity) == 0:
        return 'could not find any word of interest'
    return similarity
