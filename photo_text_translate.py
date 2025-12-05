import easyocr
from PIL import Image, ImageDraw, ImageFont
from deep_translator import GoogleTranslator

def ocr_image(image_path, lang="en"):
    try:
        reader = easyocr.Reader([lang])
        result = reader.readtext(image_path, detail=0)
        return "\n".join(result)
    except Exception as e:
        return f"OCR Error: {e}"

def translate_text_free(text, target_lang="hi"):
    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Translation Error: {e}"

def draw_translated_text_on_image(input_path, text, output_path, font_size=30):
    image = Image.open(input_path)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    draw.text((10, 10), text, font=font, fill=(255, 255, 255))
    image.save(output_path)
    return output_path
