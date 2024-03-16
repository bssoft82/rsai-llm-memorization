from faker import Faker
from rsai_logging import add_rsai_log

def get_faked_text(text, results):
    faker = Faker()
    anonymized_text = text

    for res in results:
        pii_type = res.entity_type
        pii_value = text[res.start:res.end]
        if pii_type == 'PERSON':
            anonymized_text = anonymized_text.replace(pii_value, faker.name())
        elif pii_type == 'PHONE_NUMBER':
            anonymized_text = anonymized_text.replace(pii_value, faker.phone_number())
        elif pii_type == 'ADDRESS':
            anonymized_text = anonymized_text.replace(pii_value, faker.address())
        elif pii_type == 'CAR':
            anonymized_text = anonymized_text.replace(pii_value, faker.vehicle_make_and_model())
        # Add more conditions as needed for other types of PII
    add_rsai_log (f'Anonymized Text: {anonymized_text}')
    return anonymized_text
