# German Verbs Translate From Photo  🇩🇪

Telegram bot that:
- accepts a photo with German text
- extracts text using OCR (**EasyOCR**)
- finds German verbs (**Stanza NLP**)
- removes modal verbs
- translates verbs to English (**deep_translator GoogleTranslator**)

## Tech stack
- Python
- TeleBot 
- EasyOCR
- Stanza
- GoogleTranslator (deep_translator)

## How to run

```bash
git clone https://github.com/Tarasfi/Germglish-Bot
cd Germglish-Bot
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python main.py