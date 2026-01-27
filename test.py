# import easyocr
# import stanza
# import string
# from deep_translator import GoogleTranslator
#
#
# reader = easyocr.Reader(['de'])
# result = reader.readtext("real_example2.jpg")
# verbs = [item[1] for item in result]
#
# #NLP
# nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)
#
# #Looking for verbs
# modal_verbs = {"können", "dürfen", "müssen", "wollen", "sollen", "mögen", "sein", "haben", "werden", "lassen", "geben", "machen"}
#
# unique_verbs = set()
#
# doc = nlp(" ".join(verbs))
# for sent in doc.sentences:
#     for word in sent.words:
#         if word.upos == "VERB" and word.lemma not in modal_verbs:
#
#             unique_verbs.add(word.lemma.lower())
#
# for verb in unique_verbs:
#     translated_google = GoogleTranslator(source='auto', target='en').translate(verb)
#     print(verb + " - " + translated_google)
from os.path import split

import easyocr
import stanza
import string
from deep_translator import GoogleTranslator

reader = easyocr.Reader(['de'])
result = reader.readtext("real_example2.jpg")
verbs = [item[1] for item in result]

# NLP
nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True)

# Looking for verbs
modal_verbs = {"können", "dürfen", "müssen", "wollen", "sollen", "mögen", "sein", "haben", "werden", "lassen", "geben", "machen"}

unique_verbs = set()

def clean_verb(v: str) -> str:
    if "," in v or "(" in v:
        v = split(",")[0]
    return v.strip().lower()

doc = nlp(" ".join(verbs))
for sent in doc.sentences:
    for word in sent.words:
        if word.upos == "VERB" and word.lemma not in modal_verbs:
            # unique_verbs.add(word.lemma.lower())
            cleaned = clean_verb(word.lemma)
            unique_verbs.add(cleaned)


verbs_list = list(unique_verbs)
translations = GoogleTranslator(source='de', target='en').translate_batch(verbs_list)


for de, en in zip(verbs_list, translations):
    if de or en:
        print(f"{de} - {en}")
    else:
        pass