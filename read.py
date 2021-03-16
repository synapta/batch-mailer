import csv
from io import StringIO, BytesIO
import docx

"""
Reading functions
"""


def read_docx(doc_byte):
    """
    Read doc bytes (required for form data)
    """
    doc = docx.Document(BytesIO(doc_byte))
    
    return doc


def read_csv(csv_byte):
    """
    Read csv bytes (required for form data)
    """
    csv_string = StringIO(csv_byte.decode())
    csv_reader = csv.DictReader(csv_string)
    line = 0
    
    headers = csv_reader.fieldnames
    
    data = []
    for row in csv_reader:
        data.append(row)
        line+=1
    print('    Processed %d lines' % line)

    csv_data = dict()
    csv_data['headers'] = headers
    csv_data['data'] = data

    return csv_data
