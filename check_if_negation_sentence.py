import spacy
nlp = spacy.load("en_core_web_sm")

def check_negation_sentence(user_text):
    doc = nlp(user_text)
    if [tok for tok in doc if tok.dep_ == 'neg']:
        return True
    else:
        return False