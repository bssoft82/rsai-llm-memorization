import yaml

class Config:
    log_file = None
    open_ai_api_key = None

    def __init__(self):
        with open("config/rsai_config.yaml", 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)

            Config.seed_value = cfg['seed']

            Config.open_ai_api_key = cfg['open_ai']['api_key']

            Config.log_file = cfg['logging']['log_file']
            Config.print_to_console = cfg['logging']['print_to_console']

            Config.input_data = cfg['input']['model_input_csv']
            
            Config.model_output_csv = cfg['output']['model_output_csv']
            Config.output_columns = cfg['output']['output_columns']


    @staticmethod
    def get_log_file():
        return Config.log_file

    @staticmethod
    def get_open_ai_api_key():
        return Config.open_ai_api_key

    @staticmethod
    def get_print_to_console():
        return Config.print_to_console