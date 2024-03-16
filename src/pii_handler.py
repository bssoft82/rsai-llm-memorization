from presidio_analyzer import AnalyzerEngine

from rsai_logging import add_rsai_log

def get_pii_info (text):
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(text=text,
                            language='en')
    for res in results:
         add_rsai_log(f'PII Info: {res}')
    #add_rsai_log(f'PII Info: {results}')
    return results
