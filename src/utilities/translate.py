from google_trans_new import google_translator  


def translate(lang,text):
    translator = google_translator()
    translate_text = translator.translate(text, lang_tgt=lang)
    return translate_text
      

