# Intialize the environment
python -m create venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt

# Change the openai api key
open config/rsai_config.yaml
change api_key value with your openai key value
<your openai key could be set/found at this location https://platform.openai.com/api-keys>

# Execute the Program
python src/rsai.py

# Viewing the results
### CSV file
open output/rsai_output.csv file and you can compare the output of models from this program
### Log file
open logs/rsai_logs.log to view the logs for each run
