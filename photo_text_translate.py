import pytesseract
from PIL import Image, ImageDraw, ImageFont
from googletrans import Translator

# ---------------------------
# 1. OCR FUNCTION (IMAGE → TEXT)
# ---------------------------
def ocr_image(image_path, lang="eng"):
    # SET TESSERACT PATH IF NEEDED
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    try:
        text = pytesseract.image_to_string(Image.open(image_path), lang=lang)
        return text.strip()
    except Exception as e:
        return f"Error in OCR: {e}"

# ---------------------------
# 2. TRANSLATION FUNCTION
# ---------------------------
def translate_text_free(text, target_lang="hi"):
    try:
        translator = Translator()
        result = translator.translate(text, dest=target_lang)
        return result.text
    except Exception as e:
        return f"Translation Error: {e}"

# ---------------------------
# 3. WRITE TRANSLATED TEXT ON IMAGE
# ---------------------------
def draw_translated_text_on_image(input_path, text, output_path, font_size=30):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)

    # Use default font
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    x, y = 10, 10
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    image.save(output_path)
    return output_path
