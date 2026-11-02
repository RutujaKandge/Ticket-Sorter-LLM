
from groq import Groq

# Connect to Groq API
client = Groq()

# Send a message to the LLM
response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "user",
            "content": "Say hello in Marathi."
        }
    ],
    temperature=0
)

print("Groq API Connected Successfully!")
print("LLM Response:", response.choices[0].message.content)

