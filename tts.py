from gtts import gTTS


class Tts:
    def text_to_speech(language, promt):
        try:
            myobj = gTTS(text=text, lang=language, slow=False)
            myobj.save("audio.mp3")
        except Exception:
            myobj = gTTS(text='Внимание! Ошибка в запросее', lang='ru',
                         slow=False)
            myobj.save("audio.mp3")
