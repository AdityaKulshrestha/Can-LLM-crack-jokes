import os 
from google import genai
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from datasets import Dataset

load_dotenv()


class Topics(BaseModel):
    topics: List[str]


def generate_topics():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents="Generate a list of 500 topics for joke. The topics should be funny and imaginative. The topics should be in the form of a list of strings. Topics should have both type including context and one word topics. Short context topics like: nodjs loked in a VM or AI trying to understand sarcasm and uniword topics like penguin or engineer.",
        config={
            "response_mime_type": "application/json",
            "response_schema": list[Topics],
        },
    )

    topics = response.parsed[0].topics
    return topics


def push_to_hf(topics: List[str]):
    topics_dict = {"topics": [f"Write a joke on {topic}" for topic in topics]}
    df = Dataset.from_dict(topics_dict)
    df = df.train_test_split(test_size=0.1, seed=42)
    df['train'].push_to_hub("Aditya02/Jokes", split='train')
    df['test'].push_to_hub("Aditya02/Jokes", split='test')


def main():
    topics = generate_topics()
    push_to_hf(topics)


if __name__ == "__main__":
    main()
