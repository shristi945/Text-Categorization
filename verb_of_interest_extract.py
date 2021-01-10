# verb dictionry
def create_VOI():
    verbs_of_interest = ['buy', 'take', 'aquire', 'possess', 'have', 'own']
    verbs_of_interest_df = pd.DataFrame()
    verbs_of_interest_df['head_word'] = verbs_of_interest
    verbs_of_interest_df['BOW'] = None
    for i in range(len(verbs_of_interest_df)):
        bow = []

        for synset in wn.synsets(verbs_of_interest_df['head_word'][i]):
            for j in range(len(synset.lemma_names())):
                bow.append(synset.lemma_names()[j])
        verbs_of_interest_df['BOW'][i] = set(bow)

    return verbs_of_interest_df



def findVOI():

    verbs_of_interest_df = create_VOI()