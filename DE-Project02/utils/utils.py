from gingerit.gingerit import GingerIt


def spellChecker(query):
    '''
    :param query: search query
    :return: 'query' and 'correctText' or else None
    '''
    result = GingerIt().parse(query)
    corrections = result['corrections']
    correctText = result['result']

    print("Correct Text:", corrections)
    for i in range(len(result['corrections'])):
        # print(result['corrections'][i]['start'])
        if result['corrections'][i]['start'] > 0:
            return correctText



# a= spellChecker('wate')

# import nltk
# from nltk.corpus import stopwords
# from nltk.stem import PorterStemmer
#
# nltk.download('stopwords')
#
#
# def preprocess(text):
#     # Tokenize the input
#     words = nltk.word_tokenize(text)
#
#     # Remove stop words
#     stop_words = set(stopwords.words('english'))
#     filtered_words = [word for word in words if word.casefold() not in stop_words]
#
#     # Stem the remaining words
#     stemmer = PorterStemmer()
#     stemmed_words = [stemmer.stem(word) for word in filtered_words]
#
#     return stemmed_words

def word_freq(keyword, data):
    for i in data:
        # Convert the string to lowercase for case-insensitive search
        string = i[4].lower()

        # Split the string into words
        words = string.split()

        # Count the frequency of the word in the list of words
        frequency = words.count(keyword.lower())
        i.append(frequency)

    data.sort(key=lambda x: x[-1], reverse=True)
    return data
