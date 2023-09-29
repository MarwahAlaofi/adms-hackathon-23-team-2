import openai

# Class to generate completions using GPT-3
class GPT3Completion:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key  # Set API key for OpenAI library

    # Generate text completions
    def generate_completions(self, model="gpt-3.5-turbo", prompt="", temperature=1, max_tokens=1000):
        completions = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completions.choices[0].message.content  # Return only the generated content
