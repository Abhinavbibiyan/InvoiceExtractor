import streamlit as st
import os
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input, images, prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    # Combine the images data into one list for the model input
    model_input = [input] + images + [prompt]
    response = model.generate_content(model_input)
    return response.text

def input_image_setup(uploaded_files):
    image_parts_list = []
    for uploaded_file in uploaded_files:
        if uploaded_file is not None:
            bytes_data = uploaded_file.getvalue()
            image_parts = {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
            image_parts_list.append(image_parts)
        else:
            raise FileNotFoundError("No file uploaded")
    return image_parts_list

st.set_page_config(page_title="Gemini Image Invoice Extractor")

st.header("Gemini Application")
input = st.text_input("Input Prompt: ", key="input")
uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    images = [Image.open(file) for file in uploaded_files]
    for image in images:
        st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me about the images")

input_prompt = """
               You are an expert in understanding invoices.
               You will receive input images as invoices &
               you will have to answer questions based on the input image
               """

if submit:
    image_data = input_image_setup(uploaded_files)
    response = get_gemini_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)