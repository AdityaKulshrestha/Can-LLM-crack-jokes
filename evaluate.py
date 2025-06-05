import nltk
import json
import time
import os
from tqdm import tqdm
from rouge_score import rouge_scorer
# nltk.download('punkt_tab')  # Only once
from nltk.tokenize import sent_tokenize
from typing import List 
from google import genai
from dotenv import load_dotenv
from pydantic import BaseModel
from groq import Groq
from prompts import EVAL_PROMPT, COMPLETION_PROMPT

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


class Score(BaseModel):
    Originality: int
    Timing_and_Structure: int
    Surprise_Element: int
    Clarity: int
    Impact: int
    Explanation: str
    Final_Score: float


class JokeCompletion(BaseModel):
    jokes: List[str]


def get_gemini_completion(inputs, response_schema):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash-preview-05-20",
        contents=inputs,
        config={
            "response_mime_type": "application/json",
            "response_schema": response_schema
        },
    )
    return response.parsed


def get_groq_completion(inputs, model='llama3-70b-8192'):
    chat_completion = groq_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": inputs,
            }
        ],
        # model='llama-3.3-70b-versatile',      # Exhausted
        model=model,
        response_format={"type": "json_object"}
    )
    response = chat_completion.choices[0].message.content
    return json.loads(response)


def retry_call(func, max_retries=3, delay=2, **kwargs):
    for attempt in range(max_retries):
        try:
            return func(**kwargs)
        except Exception as e:
            print(f"[Retry {attempt+1}] Failed: {e}")
            time.sleep(delay)
    raise RuntimeError(f"Function {func.__name__} failed after {max_retries} attempts")


def safe_get_groq(prompt, model):
    return retry_call(get_groq_completion, inputs=prompt, model=model)

def safe_get_gemini(prompt, schema):
    return retry_call(get_gemini_completion, inputs=prompt, schema=schema)


def compute_rouge_l(reference, candidate):
    scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
    score = scorer.score(reference, candidate)
    return score['rougeL'].fmeasure


def split_sentences(joke, num_sentences=1):
    """
    Masks out the rest of the joke

    Args:
    joke: Joke (str)
    num_sentences: Number of sentences to be masked out from the last
    """
    # Extract joke
    if "\n\n" in joke:
        joke = joke.split("\n\n")[1]
    sentences = sent_tokenize(joke)
    if num_sentences != len(sentences):
        # Number of sentences matches the lenght of the sentences which needs to be trimmed. Hence trimming the last sentence only.
        num_sentences = -1
    if len(sentences) > 1:
        partial_joke = " ".join(sentences[:-num_sentences])
    else:
        partial_joke = sentences[0][:len(sentences[0])//2]
    return partial_joke


def load_jokes(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data


def main():
    # Evaluating baseline score
    # file_path = "jokes_baselines.json"
    # output_file = 'eval_response/baseline_evaluation.json'

    # Evaluating Plansearch based jokes
    file_path = "plan_search_jokes.json"
    output_file = 'eval_response/plan_search_jokes_evaluation.json'


    # Extract the joke
    data = load_jokes(file_path)
    evaluated_reponses = []
    for item in tqdm(data):
        joke = item['joke']
        topic = item['topic']
        impartial_joke = split_sentences(joke)
        eval_prompt = EVAL_PROMPT.format(topic=topic, joke=joke)

        # Evaluate the joke
        score = get_gemini_completion(eval_prompt, Score)
        item['quality_score'] = [dict(score)]
        # Llama 8B evaluation
        llama_scores = safe_get_groq(eval_prompt, "llama3-8b-8192")
        # llama_scores = json.loads(llama_response)

        # Gemma 9B evaluation
        gemma_scores = safe_get_groq(eval_prompt, "gemma2-9b-it")
        # gemma_scores = json.loads(gemma_response)

        # Qwen Evaluation
        qwen_scores = safe_get_groq(eval_prompt, "qwen-qwq-32b")
        # qwen_scores = json.loads(qwen_response)

        item['quality_score'].extend([llama_scores, gemma_scores, qwen_scores])

        # Evaluate the novelty of the joke
        completion_prompt = COMPLETION_PROMPT.format(topic=topic, joke=impartial_joke)

        # Send the joke to gemini evaluation
        joke_completions = get_gemini_completion(completion_prompt, JokeCompletion).jokes

        # print(joke_completion)
        novelty_scores = [compute_rouge_l(joke, partial_joke) for partial_joke in joke_completions]
        max_matched_score = max(novelty_scores)
        item['novelty_score'] = {
            'completions': joke_completions,
            'scores': novelty_scores,
            'max_similar': joke_completions[novelty_scores.index(max_matched_score)],
            'max_score': max_matched_score,
        }
        evaluated_reponses.append(item)
        time.sleep(5)

    with open(output_file, 'w') as f:
        json.dump(evaluated_reponses, f, indent=4)








if __name__ == "__main__":
    main()