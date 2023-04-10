from translate import Translator

def trns(word = None, lang = 'en-ru', file = None):
    fromlang, tolang = lang.split('-')
    if file:
        with open("data/trans.txt", encoding='utf-8') as f:
            word = ' '.join(list(map(str.strip, f.readlines())))
    translator = Translator(to_lang=tolang, from_lang=fromlang)
    translation = translator.translate(word)
    return translation

print(trns(file=True))