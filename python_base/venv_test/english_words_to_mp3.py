from gtts import gTTS
from googletrans import Translator
fp = open('e:\\0\\english_words.txt', mode='r', buffering=-1, encoding="utf-8", errors=None, newline=None, closefd=True, opener=None)
words = fp.readlines()
language = 'en'
npp = 0
for word in words:
    npp+=1
    if npp<795:
        continue
    word = word.replace('\n','')
    myobj = gTTS(text=word, lang=language, slow=False)
    myobj.save(f'e:\\0\\english_words_mp3\\{npp}_{word}.mp3')
    translator = Translator()
    result = translator.translate(word, src=language, dest='ru')
    word_rus = result.text;
    myobj = gTTS(text=word_rus, lang='ru', slow=False)
    myobj.save(f'e:\\0\\english_words_mp3\\{npp}_{word}_rus.mp3')
    print (npp)



