import google.generativeai as genai
from prompt import prompt
from teststory import story
import json

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 40000,
  "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=prompt,
)

# Generate the output
response = model.generate_content(story)
print(response.text)
