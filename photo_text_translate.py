import easyocr
from PIL import Image
from deep_translator import GoogleTranslator

# Initialize EasyOCR reader globally for better performance
reader = easyocr.Reader(['en', 'hi', 'bn', 'ta', 'te', 'ml', 'kn', 'or', 'as', 'ne'])

def ocr_image(image, lang="en"):
    """
    Perform OCR on a PIL image.
    :param image: PIL Image object
    :param lang: language code for OCR (EasyOCR)
    :return: extracted text
    """
    try:
        # EasyOCR can work directly with PIL Image
        result = reader.readtext(image, detail=0)
        return "\n".join(result)
    except Exception as e:
        return f"OCR Error: {e}"

def translate_text_free(text, target_lang="hi"):
    """
    Translate text to target language using deep-translator.
    :param text: string
    :param target_lang: target language code
    :return: translated text
    """
    try:
        return GoogleTranslator(source="auto", target=target_lang).translate(text)
    except Exception as e:
        return f"Translation Error: {e}"
