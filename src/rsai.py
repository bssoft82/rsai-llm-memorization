from datetime import datetime
import random
from openai import OpenAI
import pandas as pd
import csv
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import os

from adversarial import get_adversarial_prompt
from anonymization_handler import get_anonymized_text
from data_handler import load_data, load_training_data
from faker_handler import get_faked_text
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
#df_confession_messages = load_data(Config.confessions_data)[:100]
#csvfile_10 = open ('data/rsai_confession_input_10.csv', 'a', newline='')
#df_confession_messages.to_csv (csvfile_10, index = False, header = False)

#df_essays = load_data('data/pii-detection-removal-from-educational-data/train.json')[:10]
#csvfile_10 = open ('data/essays.csv', 'a', newline='')
#df_essays.to_csv (csvfile_10, index = False, header = False)
#add_rsai_log (df_essays.describe())

df_trainings = load_training_data('data/training.1600000.processed.noemoticon.csv')[:10]
frames = [df_messages, df_trainings]
df_messages = pd.concat(frames)
# csvfile_10 = open ('data/training.csv', 'a', newline='')
# df_trainings.to_csv (csvfile_10, index = False, header = False)
add_rsai_log (df_messages.describe())
add_rsai_log (df_messages.columns)
add_rsai_log  (df_messages.head())

#for idx, message in df_messages.iterrows():
for idx, message in df_messages.iterrows():
     message_text = message['message_text']
     original_prompt = [{"role": "user", "content": message_text}]

     # Get PII Info in the messages
     #pii_info = get_pii_info (message_text)
     #human_pii_info = pii_info
     human_pii_info, pii_info = get_pii_info (message_text)
     if not pii_info:
         continue
     #human_pii_info = message['pii_info']
     add_rsai_log(f'Message Text: {message_text} \n Human PII Info: {human_pii_info}')
     
     
     # Get Adversarial Prompt
     adversarial_prompt = get_adversarial_prompt(message_text, human_pii_info)

     # Get Anonymized Prompt
     anonymized_prompt = get_adversarial_prompt (get_anonymized_text (message_text, pii_info), human_pii_info)

     # Get Faked Data Prompt
     faked_data_prompt = get_adversarial_prompt (get_faked_text (message_text, pii_info), human_pii_info)
     
     # Set the models list
     models = ["gpt-3.5-turbo-16k-0613", "gpt-4"]
     #models = []
     
     df_output = pd.concat([df_output, 
                            pd.DataFrame([{
                                'original_message': message_text,
                                'human_pii_info': human_pii_info,
                                'automated_pii_info': pii_info,
                                'adversarial_message': adversarial_prompt,
                                'anonymized_message': anonymized_prompt,
                                'faked_data_message': faked_data_prompt,
                                'org_gpt-3.5-turbo-16k-0613_output': '',
                                'org_gpt-4_output': '',
                                'adv_gpt-3.5-turbo-16k-0613_output': '',
                                'adv_gpt-4_output': '',
                                'anonymized_gpt-3.5-turbo-16k-0613_output': '',
                                'anonymized_gpt-4_output': '',
                                'faked_gpt-3.5-turbo-16k-0613_output': '',
                                'faked_gpt-4_output': '',
                        }])
                    ], ignore_index=True)
     
     output_types = ['org', 'adv', 'anonymized', 'faked']
     messages = [original_prompt, adversarial_prompt, anonymized_prompt, faked_data_prompt]
     for model in models:
        for i in range(len(output_types)):
                # response = 'Test_Mode_output. Model not triggered'
                response = get_inference(client, model, messages[i])
                df_output.at[df_output.index[-1], f'{output_types[i]}_{model}_output'] = response
                add_rsai_log (f'{output_types[i]}_message: {messages[i]} \n model: {model} \n response: {response}')

df_output.to_csv (csvfile, index = False, header = False)
csvfile.close()