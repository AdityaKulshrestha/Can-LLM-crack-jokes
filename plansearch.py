import json 
import time 
from tqdm import tqdm
import os
from google import genai
from datasets import load_dataset
from groq import Groq
from prompts import PROMPT_1, PROMPT_2, PROMPT_3, EVAL_PROMPT
from dotenv import load_dotenv

load_dotenv()


groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def get_groq_completion(inputs):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": inputs,
            }
        ],
        # model='llama-3.3-70b-versatile',      # Exhausted
        model='llama3-70b-8192'
    )
    return chat_completion.choices[0].message.content


def get_gemini_completion(inputs, response_schema):
    response = gemini_client.models.generate_content(
        model="gemini-2.0-flash",
        contents=inputs,
        config={
            "response_mime_type": "application/json",
            "response_schema": response_schema
        },
    )
    return response.text


def main():
    ds = load_dataset("Aditya02/Jokes")
    df_test = ds['test']

    # Testing on sample
    # df_test = df_test.select(range(5))

    jokes = []

    for idx in tqdm(df_test):
        topic = idx['topics'].replace("Write a joke on", "")
        idea_prompt = PROMPT_1.format(topic=topic)
        ideas = get_groq_completion(idea_prompt)
        time.sleep(2)
        refined_ideas_prompt = PROMPT_2.format(topic=topic, ideas=ideas)
        refined_ideas = get_groq_completion(refined_ideas_prompt)
        time.sleep(2)
        joke_prompt = PROMPT_3.format(topic=topic, ideas=refined_ideas)
        joke = get_groq_completion(joke_prompt)
        print(joke)
        jokes.append(
            {

                'topic': topic,
                'idead': ideas,
                'refined_ideas': refined_ideas,
                'joke': joke
            }
        )

        with open('plan_search_jokes.json', 'w') as f:
            json.dump(jokes, f, indent=4)


if __name__ == "__main__":
    main()