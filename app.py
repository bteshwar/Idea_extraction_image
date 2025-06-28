import streamlit as st
from openai import OpenAI
from PIL import Image
import base64
import io
import os
from dotenv import load_dotenv

# Load .env for local use
load_dotenv()

# Get API Key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set Streamlit page config
st.set_page_config(page_title="Student Project Analyzer", layout="centered")

# Add serene background
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1950&q=80");
    background-size: cover;
}
[data-testid="stHeader"], [data-testid="stToolbar"] {background: rgba(0,0,0,0);}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("🧭 Student Project Analyzer")

st.markdown(
    "Upload an image of a student project sheet. "
    "The AI will extract the **Problem Statement**, **Solution**, and **Student Names**, "
    "responding in under **200 words**."
)

# Image uploader
uploaded_file = st.file_uploader("📷 Upload project image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert image to base64 for OpenAI API
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    # Prepare the vision prompt
    prompt = (
        "Analyze this image carefully. Extract the following information:\n"
        "1. Problem Statement\n"
        "2. Solution\n"
        "3. Student Names\n\n"
        "Be concise. Your entire answer must be under 200 words."
    )

    # Call OpenAI GPT-4o Vision
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ]
    )

    # Get response
    result = response.choices[0].message.content.strip()
    st.success("✅ Analysis Complete")
    st.markdown(result)
