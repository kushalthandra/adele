import openai
import pyttsx3

#read the readme.md file to learn about how to configure the api key
openai.api_key='your-api-key'

engine=pyttsx3.init()
def generate_response(prompt):
    response=openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=5000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["text"]

x=generate_response("tell me about python")
print(x)