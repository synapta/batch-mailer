import csv
import docx

"""
Reading functions
"""


def read_docx(file_path):
    doc = docx.Document(file_path)
    
    return doc


def read_csv(file_path):
    print('\nReading %s... ' % file_path)

    with open(file_path, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
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
