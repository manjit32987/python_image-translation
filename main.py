import streamlit as st
from PIL import Image
import tempfile
from photo_text_translate import (
    ocr_image,
    translate_text_free,
    draw_translated_text_on_image,
)

st.title("📸 Photo → Text → Translation System")

mode = st.radio(
    "Choose Mode:",
    ["Upload Photo", "Use Camera"],
    index=0
)

tess_lang = st.text_input("OCR Language (EasyOCR code)", value="en")
target_lang = st.text_input("Translate to (e.g., en, hi, bn, ta, fr)", value="hi")
font_size = st.slider("Overlay font size", 20, 80, 30)

# ---------------------------
# MODE 1: UPLOAD PHOTO
# ---------------------------
image = None
if mode == "Upload Photo":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

# ---------------------------
# MODE 2: CAMERA INPUT
# ---------------------------
elif mode == "Use Camera":
    camera_img = st.camera_input("Capture a photo")
    if camera_img:
        image = Image.open(camera_img)
        st.image(image, caption="Captured from Camera", use_column_width=True)

# ---------------------------
# PROCESS OCR + TRANSLATE
# ---------------------------
if image and st.button("Process Image"):
    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
        image.save(temp.name)
        img_path = temp.name

    extracted_text = ocr_image(img_path, tess_lang)

    st.subheader("📄 Extracted Text")
    st.write(extracted_text if extracted_text else "_No text found_")

    if extracted_text:
        translated = translate_text_free(extracted_text, target_lang)
        st.subheader("🌍 Translated Text")
        st.write(translated)

        # Output image
        out_path = f"output_translated.jpg"
        draw_translated_text_on_image(img_path, translated, out_path, font_size=font_size)

        st.subheader("🖼️ Image with Translated Text")
        st.image(out_path, use_column_width=True)

        with open(out_path, "rb") as f:
            st.download_button("Download Result", f, file_name="translated.jpg")
