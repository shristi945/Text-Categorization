# Initiating a Flask API
from flask import Flask, render_template
from flask import request
app = Flask(__name__)

import spacy
nlp = spacy.load('en_core_web_sm')

from subject_verb_object_extract import findSVOs
from word_of_interest_extract import findWOI
from check_if_negation_sentence import  check_negation_sentence

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    # if request.method == 'POST':

        # Input text goes here

    user_text_list = [str(x) for x in request.form.values()]
    user_text = ' '.join(user_text_list)

    # user_text = "i don't have a dog"
    tokens = nlp(user_text)
    svos = findSVOs(tokens)
    negation_flag = False

    # return str(svos)
    if check_negation_sentence(user_text) == True:
        negation_flag = True

    prediction_list = findWOI(svos, user_text)
    if negation_flag:
        result = prediction_list + "sentence is in negation"
    else:
        result = prediction_list


    return render_template('index.html', prediction_text='Predicted Category : {}'.format(result))




if __name__ == "__main__":
    app.run(debug=True)
    # hello()