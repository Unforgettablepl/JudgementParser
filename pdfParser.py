import json
from pypdf import PdfReader
import google.generativeai as genai

def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def send_to_google_gemini(text, json_schema, system_instructions, api_key):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", system_instruction=system_instructions)
    response = model.generate_content(
        text,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=json_schema
        )
    )
    return response

pdf_path = input("Enter the path to the PDF file: ")
extracted_text = extract_text_from_pdf(pdf_path)
json_schema = {
    "type": "object",
    "properties": {
        "Fine Paid": {
            "type": "integer"
        },
        "Date of Institution of Case": {
            "type": "string"
        },
        "Evidence produced by the prosecution": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "Evidence produced by the defendant": {
            "type": "array",
            "items": {
                "type": "string"
            }
        }
    },
    "required": [
        "Date of Institution of Case",
        "Evidence produced by the prosecution"
    ]
}
system_instructions = "If a fine was imposed tell how much total fine was paid by the parties involved. Also tell on what date was the case instituted. Also make a list of the evidences which were produced by the prosecution or the defendant."
api_key = "AIzaSyB0p_0y9EozZjX8krllmkGVNINkyccnnrA"
genai.configure(api_key=api_key)
response = send_to_google_gemini(extracted_text, json_schema, system_instructions, api_key)
content = response.text
json_response = json.loads(content)
print(json.dumps(json_response, indent=2))