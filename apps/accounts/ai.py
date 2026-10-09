from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

while True:
    question = input("You: ")

    if question.lower() == "exit":
        break

    response = client.interactions.create(
        model="gemini-3.8-flash",
        input=question
    )

    print("Answer:", response.output_text)