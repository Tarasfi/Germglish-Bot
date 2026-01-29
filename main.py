from dotenv import load_dotenv
import telebot
import os
import easyocr
import stanza
from deep_translator import GoogleTranslator

load_dotenv()

#Telebot API
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Stanza
nlp = stanza.Pipeline(lang='de', processors='tokenize,mwt,pos,lemma', tokenize_pretokenized=True, use_gpu=False)


#Not necessary words
modal_verbs = {"können", "dürfen", "müssen", "wollen", "sollen", "mögen", "sein", "haben", "werden", "lassen", "geben", "machen"}


# OCR initialisation
reader = easyocr.Reader(['de'], gpu=False)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hi {message.chat.first_name}, send me a photo with german words!')


#Removing punctuation marks
def clean_verb(v: str) -> str:
    for sep in [",", "("]:
        if sep in v:
            v = v.split(sep)[0]
    return v.strip().lower()


@bot.message_handler(content_types=['photo'])
def main(message):
    msg = bot.reply_to(message,  "Extracting text...📝")

    # All verbs
    unique_verbs = set()

    #Getting photo from user
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    #Extracting text from photo
    result = reader.readtext(downloaded_file)
    verbs = [item[1] for item in result]

    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Finding verbs...🔎")
    #Finding verbs
    doc = nlp(" ".join(verbs))
    for sent in doc.sentences:
        for word in sent.words:
            if word.upos == "VERB" and word.lemma not in modal_verbs:
                # unique_verbs.add(word.lemma.lower())
                cleaned = clean_verb(word.lemma)
                unique_verbs.add(cleaned)

    bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Translating...🈳")

    #Translating using deep_translator
    verbs_list = list(unique_verbs)
    translations = GoogleTranslator(source='de', target='en').translate_batch(verbs_list)

    #Forming output to user
    message_text = ""
    for de, en in zip(verbs_list, translations):
        if de and en:
            message_text += f"{de} - {en}\n"

    # bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="Finding verbs" )

    #Sending output
    if message_text:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text=message_text)
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=msg.message_id, text="No verbs detected!❌")


bot.polling(none_stop=True)

