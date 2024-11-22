import crash_lang as cr
import threading
import time
import openai
import os
from openai import OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
question = None
gpt_response = None
def ask_gpt(prompt):
    try:
        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
        ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Can't access API;{e}")
        return None
    
micindex = 4 
client = OpenAI()

def textMessage():
    global question
    global gpt_response
    question = cr.google_free(micindex)
    gpt_response = ask_gpt(question)
    print("GPT Answer:", gpt_response)
    cr.speak(gpt_response,"ko")
    return question, gpt_response


if __name__ =="__main__":
    textMessage()

