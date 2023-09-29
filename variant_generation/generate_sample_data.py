from datetime import datetime
import os
import json
import pandas as pd
from GPT3Completion import GPT3Completion
from dotenv import load_dotenv
from prompts import PERSONAS

error_count = 0
def create_prompt(persona_dict):
    text = persona_dict['text']
    campaign_message = persona_dict['campaign_message']
    json_fields_str = ', '.join(persona_dict['json_fields'])
    # Create prompt according to specified format
    prompt = f"{text}\n{campaign_message}\nDo not return any text before or after the persona.\n"
    prompt += f"Respond in a json format with the following fields: {json_fields_str}.\n"
    return prompt


# Class for generating sample data
class SampleDataGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.sample_data_json_list = []  # Store generated sample data
        self.failed_sample_data = []


    # Generate samples using GPT3.5
    def generate_sample(self):
        for key in PERSONAS.keys():
            prompt = create_prompt(PERSONAS[key])
            print(f"Persona: {key}")
            try:
                gpt3_completion = GPT3Completion(self.api_key)
                sample_data = gpt3_completion.generate_completions(prompt=prompt)  # Actual sample generation
                json_sample_data = json.loads(sample_data)
                json_sample_data['persona'] = key
                self.sample_data_json_list.append(json_sample_data)
            except Exception as e:
                self.failed_sample_data.append(sample_data)
                print(f"Failed to generate sample: {e}")

    # Save generated samples to CSV
    def save_samples(self):
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"gpt-3.5-turbo-sample-data-temp-1-{timestamp}.csv"
        sample_data_df = pd.DataFrame(self.sample_data_json_list)
        sample_data_df.to_csv(filename)
        print(f"Sample data written to {filename}")

        with open("failed-sampel-data.json", "w") as f:
            json.dump(self.failed_sample_data, f)

    # Run the sample data generation
    def run(self, num_of_samples=10):
        for i in range(num_of_samples):
            print(f"generating sample {i}")
            self.generate_sample()
        self.save_samples()


# Entry point of the program
if __name__ == "__main__":
    load_dotenv("api.env")  # Load environment variables
    api_key = os.environ.get('OPENAI_API_KEY')  # Get OpenAI API key from environment variables
    sample_data_gen = SampleDataGenerator(api_key)
    sample_data_gen.run()  # Start sample data generation
