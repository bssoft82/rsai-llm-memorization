import pandas as pd
from rsai_logging import add_rsai_log


def load_data (data_path):
    df = pd.read_csv(data_path, header=0, names=['message_text', 'pii_info'])
    return df
