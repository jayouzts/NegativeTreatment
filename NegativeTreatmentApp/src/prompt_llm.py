import os
from string import Template
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Load the prompt from file once at module level
PROMPT_PATH = os.path.join(os.path.dirname(__file__), "prompts", "negative_treatment.txt")

with open(PROMPT_PATH, 'r', encoding='utf-8') as file:
    PROMPT_TEMPLATE = Template(file.read())

def analyze_negative_treatment(case_text: str) -> str:
    """
    Analyzes the given case text for negative legal treatment using an LLM.

    Args:
        case_text (str): The full opinion text.

    Returns:
        str: LLM-generated analysis of negative treatment.
    """
    prompt = PROMPT_TEMPLATE.substitute(opinion_text=case_text)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are a legal expert AI."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

# TODO: For very large opinions (e.g., lengthy Supreme Court decisions such as Dobbs, case id 15560296770592570126 ),
# the full text may exceed the token limit of the current OpenAI model and my API tier.
# In production, this should be handled by splitting the input into smaller sections
# (e.g., paragraphs or logical blocks), analyzing each separately, and then aggregating results.
# Due to time and resource constraints for this demonstration, long texts are not currently segmented.

