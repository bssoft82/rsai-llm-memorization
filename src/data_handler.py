import pandas as pd
from rsai_logging import add_rsai_log


def load_data (data_path):
    if data_path.endswith('.csv'):
        df = pd.read_csv(data_path, header=0, names=['message_text', 'pii_info'])
    elif data_path.endswith('.json'):
        df = pd.read_json(data_path, lines=True)
    else:
        add_rsai_log(f'ERROR: File type not supported. Supported file types are: csv, json')
        return None
    return df


def load_training_data(data_path):
    df = pd.read_csv(data_path, header=0, names=['target', 'ids', 'date', 'flag', 'user', 'message_text'], encoding='latin-1')
    df['pii_info'] = ''
    return df

