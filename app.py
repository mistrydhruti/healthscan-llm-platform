import streamlit as st
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ['API_KEY'])

# Create the model
generation_config = {
  "temperature": 0.6,
  "top_p": 1,
  "top_k": 32,
  "max_output_tokens": 8192,
}

system_prompt = """
    You are an advanced medical practitioner specializing in image analysis for a leading hospital. Your task is to conduct a thorough examination of medical images and provide insights, findings, and recommendations with a high degree of accuracy. Your expertise will support healthcare providers in diagnosing, planning treatments, and understanding patient conditions.
    Your Responsibilities include:
    1. Detailed Analysis: Carefully examine the medical image to identify any abnormalities, health risks, or notable features relevant to the patient’s condition. Your analysis should highlight structural, functional, or textural anomalies.
    2. Findings Report: Provide a concise yet comprehensive report summarizing key observations. Mention any visible signs of disease, abnormal growths, tissue irregularities, or other significant findings. Where applicable, specify locations, sizes, and possible implications of these findings.
    3. Recommendations and Next Steps: Offer recommendations based on your analysis, such as further testing, biopsy, or specific types of imaging. Mention any specific follow-up actions required to confirm findings or understand the scope of any identified issues.
    4. Treatment Suggestions: Based on the findings, outline potential treatment options or interventions. This could range from lifestyle changes to more targeted medical or surgical treatments, depending on the type and severity of the identified condition.
    
    Important Notes:
    1. Scope of Response:Limit your response to observations and insights directly observable from the image.Avoid making assumptions beyond what the image reveals unless the context provides supporting data for hypothesis formulation.
    2. Clarity of Image: If the image clarity is poor or compromised, mention how this might affect the confidence of your analysis and suggest possible image enhancement or reimaging if necessary.
    3. Disclaimer: Remind readers that this analysis is intended to support but not replace clinical judgment. Further clinical correlation with the patient’s history and other diagnostic findings is recommended.

    Please provide me an output response with these 4 headings Detailed Analysis, Findings Report,Recommendations and Next Steps, Treatment Suggestions
    """

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

st.set_page_config(page_title="HealthScan Pro", page_icon=":robot:")
st.title("HealthScan Pro")
st.subheader("Advanced Medical Image Analysis & Diagnostic Insights")

uploaded_file = st.file_uploader("Upload the medical image for analysis", type=['png', 'jpg','jpeg'])
if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Image")
submit_button = st.button("Generate diagnosis")

if submit_button:
    image_data = uploaded_file.getvalue()
    image_parts = [
        {
            "mime_type": "image/jpeg",
            "data": image_data
        },
    ]
    prompt_parts = [
        image_parts[0],
        system_prompt,

    ]
    
    response = model.generate_content(prompt_parts)
    if response:
        st.title('Diagnosis based on provided image')
        st.write(response.text)
