import streamlit as st
from PIL import Image
import pytesseract
from googletrans import Translator
from streamlit_drawable_canvas import st_canvas

# Set tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

translator = Translator()
st.title("📸 OCR & Translation with Selectable Text Area")

# ------------------ Image Input ------------------
mode = st.radio("Choose Input Method", ["Upload Photo", "Camera"])
img = None

if mode == "Upload Photo":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)

elif mode == "Camera":
    camera_file = st.camera_input("Capture a photo")
    if camera_file:
        img = Image.open(camera_file)

# ------------------ If image loaded ------------------
if img:
    st.subheader("Select the area containing text")
    
    # Create canvas for user to draw rectangle
    canvas_result = st_canvas(
        fill_color="rgba(0,0,0,0)",  # transparent fill
        stroke_width=2,
        stroke_color="#FF0000",
        background_image=img,
        update_streamlit=True,
        height=img.height,
        width=img.width,
        drawing_mode="rect",
        key="canvas",
    )

    # Dropdown for translation language
    st.subheader("Choose Translation Language")
    lang = st.selectbox(
        "Translation Language",
        {
            "English": "en",
            "Hindi": "hi",
            "Bengali": "bn",
            "Tamil": "ta",
            "Telugu": "te",
            "Malayalam": "ml",
            "Kannada": "kn",
            "Odia": "or",
            "Assamese": "as",
            "Nepali": "ne",
            "Spanish": "es",
            "French": "fr",
            "German": "de"
        }
    )

    # ------------------ Process OCR ------------------
    if st.button("Extract & Translate"):
        if canvas_result.json_data["objects"]:
            # Take the first rectangle drawn
            rect = canvas_result.json_data["objects"][0]
            left = int(rect["left"])
            top = int(rect["top"])
            width = int(rect["width"])
            height = int(rect["height"])
            
            cropped_img = img.crop((left, top, left + width, top + height))
            
            extracted_text = pytesseract.image_to_string(cropped_img)
            st.subheader("📝 Extracted Text")
            st.text_area("Extracted Text", extracted_text, height=200)
            
            translated_text = translator.translate(extracted_text, dest=lang).text
            st.subheader("🌍 Translated Text")
            st.text_area("Translated Text", translated_text, height=200)
        else:
            st.warning("Please draw a rectangle on the image first!")
