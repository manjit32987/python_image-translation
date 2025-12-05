import streamlit as st
from PIL import Image
from photo_text_translate import ocr_image, translate_text_free
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="OCR & Translation App", layout="wide")
st.title("📸 OCR & Translation Tool")

# ------------------ Input Mode ------------------
mode = st.radio("Choose Input Method", ["Upload Photo", "Use Camera"])
img = None

if mode == "Upload Photo":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
elif mode == "Use Camera":
    camera_file = st.camera_input("Capture a photo")
    if camera_file:
        img = Image.open(camera_file)

# ------------------ If Image Loaded ------------------
if img:
    st.subheader("Select the area containing text (draw rectangle)")
    
    # Drawable Canvas for selecting text area
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

    # Translation language dropdown
    st.subheader("Choose Translation Language")
    lang = st.selectbox(
        "Select language",
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

    if st.button("Extract & Translate"):
        if canvas_result.json_data["objects"]:
            # Take the first rectangle drawn
            rect = canvas_result.json_data["objects"][0]
            left = int(rect["left"])
            top = int(rect["top"])
            width = int(rect["width"])
            height = int(rect["height"])
            
            cropped_img = img.crop((left, top, left + width, top + height))
            
            extracted_text = ocr_image(cropped_img)
            st.subheader("📝 Extracted Text")
            st.text_area("Extracted Text", extracted_text, height=200)
            
            translated_text = translate_text_free(extracted_text, target_lang=lang)
            st.subheader("🌍 Translated Text")
            st.text_area("Translated Text", translated_text, height=200)
        else:
            st.warning("Please draw a rectangle on the image first!")
