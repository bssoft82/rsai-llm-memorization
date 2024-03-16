from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

from rsai_logging import add_rsai_log

def get_anonymized_text (text, results):
    # Analyzer results are passed to the AnonymizerEngine for anonymization
    anonymizer = AnonymizerEngine()
    anonymized_text = anonymizer.anonymize(text=text, analyzer_results=results)
    add_rsai_log(f'Anonymized Text: {anonymized_text}')
    return anonymized_text

def get_pii_info (text):
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(text=text,
                            language='en')
    for res in results:
         add_rsai_log(f'PII Info: {res}')
    #add_rsai_log(f'PII Info: {results}')
    return results
