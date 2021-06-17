from gingerit.gingerit import GingerIt

def check_grammar(text):
    parser = GingerIt()
    correct_text = parser.parse(text)
    return correct_text['result']