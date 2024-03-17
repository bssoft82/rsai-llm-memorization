from presidio_analyzer import AnalyzerEngine

from rsai_logging import add_rsai_log

def get_pii_info (text):
    analyzer = AnalyzerEngine()
    results = analyzer.analyze(text=text,
                            language='en')
    pii_names = [res.entity_type for res in results]
    #names_object = {"pii_names": pii_names}
    add_rsai_log(f'PII names: {pii_names}')
    for res in results:
         add_rsai_log(f'PII Info: {res}')
    #add_rsai_log(f'PII Info: {results}')
    return ",".join(pii_names), results
