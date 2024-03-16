from presidio_anonymizer import AnonymizerEngine, OperatorConfig
from rsai_logging import add_rsai_log

def get_anonymized_text (text, results):
    # Analyzer results are passed to the AnonymizerEngine for anonymization
    anonymizer = AnonymizerEngine()
    operators={"PERSON": OperatorConfig(operator_name="replace", 
                                    params={"new_value": "REPLACED_NAME"}),
           "LOCATION": OperatorConfig(operator_name="mask", 
                                      params={'chars_to_mask': 10, 
                                              'masking_char': '*',
                                              'from_end': True}),
           "DEFAULT": OperatorConfig(operator_name="redact")}
    
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results, operators=operators).text
    
    add_rsai_log(f'Anonymized Text: {anonymized_text}')
    return anonymized_text
