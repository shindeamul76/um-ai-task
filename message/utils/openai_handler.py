import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generate_prompt(history_prompt, content, style_prompt):
    """
    Generate the complete prompt for OpenAI GPT based on history and user style.
    """
    return f"Conversation history:\n{history_prompt}\nRespond to the last message: '{content}'. Use this user's style: {style_prompt}"

def fetch_gpt_response(openai_prompt, max_tokens=100, temperature=0.3):
    """
    Call the OpenAI API to fetch a GPT response.
    """
    total_token_limit = 4096  
    prompt_tokens = len(openai_prompt.split())  
    max_tokens = min(max_tokens, total_token_limit - prompt_tokens)

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": "Provide meaningful responses while mimicking the user's style."},
            {"role": "user", "content": openai_prompt},
        ],
    )
    return response['choices'][0]['message']['content']