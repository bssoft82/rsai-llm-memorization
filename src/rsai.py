from datetime import datetime
import random
from openai import OpenAI
import pandas as pd
import csv
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import os

from adversarial import get_adversarial_prompt
from data_handler import load_data
from inference_handler import get_inference
from pii_handler import get_pii_info
from rsai_logging import add_rsai_log, initlogging
from config import Config

# Initialize the configuration
config = Config()
initlogging(config.get_log_file())

# Set the seed value
random.seed(config.seed_value)

# Set openai api key. Shall this be moved to the inference handler?
os.environ['OPENAI_API_KEY'] = config.get_open_ai_api_key()
client = OpenAI()

# Output file
csvfile = open (config.model_output_csv, 'a', newline='')
df_output = pd.DataFrame(columns=config.output_columns)

# Load data
df_messages = load_data(Config.input_data)

for idx, message in df_messages.iterrows():
     message_text = message['message_text']
     human_pii_info = message['pii_info']
     add_rsai_log(f'Message Text: {message_text} \n Human PII Info: {human_pii_info}')
     
     # Get PII Info in the messages
     pii_info = get_pii_info (message_text)
     
     # Get Adversarial Prompt
     adversarial_prompt = get_adversarial_prompt (message_text, human_pii_info)
     
     # Set the models list
     models = ["gpt-3.5-turbo-16k-0613", "gpt-4"]
     df_output = pd.concat([df_output, pd.DataFrame([{'original_message': message_text,
                    'adversarial_message': adversarial_prompt,
                    'pii_info': human_pii_info,
                    'gpt-3.5-turbo-16k-0613_output': '',
                    'gpt-4_output': ''}])], ignore_index=True)
     
     for model in models:
        response = get_inference(client, model, adversarial_prompt)
        #response = 'Test_Fmwk'
        df_output.at[df_output.index[-1], f'{model}_output'] = response
        add_rsai_log (f'model: {model} \n response: {response}')

df_output.to_csv (csvfile, index = False, header = False)

# seed_val = 42
# run_gpt = False
# if run_gpt:
#     OUTPUT_FILE_CSV = './output/model_output.csv'
#     with open(OUTPUT_FILE_CSV, 'a', newline='') as csvfile:
#         for msg in messages:
#             add_rsai_log("_"*25)
#             add_rsai_log (f'prompt: {msg}')
#             timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             for model in models:
#                 random.seed(seed_val)
#                 response = get_inference(model, msg)
#                 add_rsai_log (f'model: {model} \n response: {response}')
#                 spamwriter = csv.writer(csvfile, delimiter=',')
#                 spamwriter.writerow([timestamp, msg, model, response.content])


