# Intialize the environment
python -m create venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt

# Change the openai api key
Open _config/rsai_config.yaml_.
Change _api_key_ value with your openai key value
Your openai key could be set/found at this location: https://platform.openai.com/api-keys

# Execute the Program
python src/rsai.py

# Viewing the results
### CSV file
Open _output/rsai_output.csv_ file and you can compare the output of models from this program
### Log file
Open _logs/rsai_logs.log_ to view the logs for each run
