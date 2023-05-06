# # from textblob import Spelling
# from textblob import TextBlob
# a = "New yor city"  # incorrect spelling
# print("original text: " + str(a))
#
# b = TextBlob(a)
#
# # prints the corrected spelling
# print("corrected text: " + str(b.correct()))
#

print("%"*200)
#
#
# from spellchecker import SpellChecker
# spell = SpellChecker(language='en')
# # find those words that may be misspelled
# misspelled = spell.unknown([a])
# print("misspelled text: ",misspelled)
# for word in misspelled:
# 	# Get the one `most likely` answer
# 	print(spell.correction(word))
# #
# 	# Get a list of `likely` options
# 	print(spell.candidates(word))
#
#
#
# from autocorrect import Speller
#
# spell = Speller(lang='en')
# #
# print(spell('caaaar'))
# print(spell('mcssage'))
# print(spell('iphon pr'))
# print(spell("instagrm"))
#
# print('*'*200)




#
# from textblob.en import Spelling
#
# spell = Spelling()
#
# text = "newYor City"
# words = TextBlob(text).words
# print(words)
#
# for word in words:
#     corrected_word = spell.correction(word)
#     if word != corrected_word:
#         print(f"Original word: {word}, Corrected word: {corrected_word}")





from gingerit.gingerit import GingerIt

def spellChecker(query):
  query = 'iphne 14 pr'
  result = GingerIt().parse(query)
  corrections = result['corrections']
  correctText = result['result']

  print("Correct Text:",correctText)
  print('*'*100)
  print("CORRECTIONS",result)
  for i in range(len(result['corrections'])):
    print(result['corrections'][i]['start'])
    if result['corrections'][i]['start'] >0:
      return {'query':query ,'correctText':correctText}


# print('*' * 100)
# for d in corrections:
#   print("________________")
#   print("Previous:",d['text'])
#   print("Correction:",d['correct'])
#   print("`Definiton`:",d['definition'])



# spellChecker(a)

# # Create a corrector
# corrector = jamspell.TSpellCorrector()
#
# # Load Language model -
# # argument is a downloaded model file path
# corrector.LoadLangModel('Downloads/en_model.bin')
#
# # To fix text automatically run FixFragment:
# print(corrector.FixFragment('I am the begt spell cherken!'))
#
# # To get a list of possible candidates
# # pass a splitted sentence, and a word position
# print(corrector.GetCandidates(['i', 'am', 'the', 'begt', 'spell', 'cherken'], 3))
#
# print(corrector.GetCandidates(['i', 'am', 'the', 'begt', 'spell', 'cherken'], 5))
