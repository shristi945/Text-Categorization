import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import wordnet as wn
lemmatizer = nltk.WordNetLemmatizer()
from nltk.corpus import stopwords

import spacy
nlp = spacy.load('en_core_web_sm')

import pandas as pd

from similarity_with_WOI import findSimilarWOI

def create_WOI():
    head_words_of_interest = ['car', 'sports', 'fitness', 'gym', 'food', 'pets', 'gaming', 'tech', 'reading']

    word_of_interest = {}

    for word in head_words_of_interest:
        is_a_list, instance_of_list = [], []

        for synset in wn.synsets(word):
            for i in range(len(synset.lemma_names())):
                is_a_list.append(str(synset.lemma_names()[i]).lower())
            for hypo in synset.hyponyms():
                for j in range(len(hypo.lemmas())):
                    instance_of_list.append(str(hypo.lemmas()[j].name()).lower())
            word_of_interest[word] = {'is_a_list': is_a_list, 'instance_of_list': instance_of_list}

    for key, value in word_of_interest.items():
        for i in range(len(word_of_interest[key]['is_a_list'])):
            word_of_interest[key]['is_a_list'][i] = ' '.join(word_of_interest[key]['is_a_list'][i].split('_'))
        for j in range(len(word_of_interest[key]['instance_of_list'])):
            word_of_interest[key]['instance_of_list'][j] = ' '.join(
                word_of_interest[key]['instance_of_list'][j].split('_'))

    word_of_interest_df = pd.DataFrame()
    word_of_interest_df['head_word'] = head_words_of_interest
    word_of_interest_df['is_a_list'] = None
    word_of_interest_df['instance_of_list'] = None

    for i in range(len(word_of_interest_df)):
        if word_of_interest_df['head_word'][i] in word_of_interest:
            word_of_interest_df['is_a_list'][i] = word_of_interest[word_of_interest_df['head_word'][i]]['is_a_list']
            word_of_interest_df['instance_of_list'][i] = word_of_interest[word_of_interest_df['head_word'][i]]['instance_of_list']

    for i in range(len(word_of_interest_df)):
        word_of_interest_df['is_a_list'][i] = set(word_of_interest_df['is_a_list'][i])
        word_of_interest_df['instance_of_list'][i] = set(word_of_interest_df['instance_of_list'][i])

    return word_of_interest_df


def remove_stopward_from_obj(obj):
    text_tokens = word_tokenize(obj)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
    obj_token = []
    doc = nlp(obj)
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN']:
            obj_token.append(token.text)

    if len(obj_token):
        return obj_token
    else:
        return tokens_without_sw
    
def findMaxSimilarity(similarity):

    sorted_key_list = sorted(similarity, key=similarity.get, reverse=True)
    top_key_list = sorted_key_list[0]
    if len(top_key_list):
        return top_key_list
    else:
        return sorted_key_list

def printHeirarchy():
    pass

def findWOI(list_of_tuple, user_text):
    # check if subject or object contains any words of interest
    # words of interest (list of all the words of interest as well as related words)
    # if yes, find head word of interest

    result_word_of_interest = []
    similarity  = {}
    word_of_interest_df = create_WOI()

    if len(list_of_tuple):
        for tuples in list_of_tuple:
            obj_word_list = remove_stopward_from_obj(tuples[2])
            for obj in obj_word_list:
                for i in range(len(word_of_interest_df)):
                    if obj.lower() in word_of_interest_df['is_a_list'][i] or obj.lower() in word_of_interest_df['instance_of_list'][i]:
                        # print(word_of_interest_df['head_word'][i])
                        result_word_of_interest.append(word_of_interest_df['head_word'][i])
                        if len(result_word_of_interest) > 0:
                            break

                    # if not direct match then find similarity between object and headword also object and related words
                    similarity_obj_headword = findSimilarWOI(obj, word_of_interest_df['head_word'][i])
                    if similarity_obj_headword:
                        similarity[(obj, word_of_interest_df['head_word'][i])] = similarity_obj_headword

                    # finding similarity with is_a_list_word
                    for is_a_list_word in word_of_interest_df['is_a_list'][i]:
                        similarity_obj_is_a_list_word = findSimilarWOI(obj, is_a_list_word)
                        if similarity_obj_is_a_list_word:
                            similarity[(obj, word_of_interest_df['head_word'][i], is_a_list_word)] = similarity_obj_is_a_list_word

                    # finding similarity with instance_of_list
                    for instance_of_word in word_of_interest_df['instance_of_list'][i]:
                        similarity_obj_instance_of_word = findSimilarWOI(obj, instance_of_word)
                        if similarity_obj_instance_of_word:
                            similarity[(obj, word_of_interest_df['head_word'][i], instance_of_word)] = similarity_obj_instance_of_word
        
        maxSimilar = findMaxSimilarity(similarity)
        result_word_of_interest.append(maxSimilar)

    else:
        user_text_filtered = remove_stopward_from_obj(user_text)
        for i in range(len(word_of_interest_df)):
            for words in user_text_filtered:
                if words.lower() in word_of_interest_df['is_a_list'][i] or words.lower() in word_of_interest_df['instance_of_list'][i]:
                    result_word_of_interest.append(word_of_interest_df['head_word'][i])

                # if we could not find anything related to head word by looking at word by word then we find similarity to head word or related word

    return result_word_of_interest
