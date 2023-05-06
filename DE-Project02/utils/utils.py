
from gingerit.gingerit import GingerIt

def spellChecker(query):
    '''

    :param query: search query
    :return: 'query' and 'correctText' or else None
    '''
    result = GingerIt().parse(query)
    corrections = result['corrections']
    correctText = result['result']

    print("Correct Text:",corrections)
      # print('*'*100)
      # print("CORRECTIONS",result)
    for i in range(len(result['corrections'])):
        # print(result['corrections'][i]['start'])
        if result['corrections'][i]['start'] >0:
          return {'query':query ,'correctText':correctText}


#
correctSpell =spellChecker('New yor  City')
# print(correctSpell)
if correctSpell != None:
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(correctSpell['query'] , correctSpell['correctText'] )