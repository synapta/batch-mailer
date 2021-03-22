import csv
from io import StringIO, BytesIO
import docx
import openpyxl

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
    
    return csv_reader


def read_xlsx(xlsx_byte):
    """
    Read xlsx bytes (required for form data)
    """
    xlsx_io = BytesIO(xlsx_byte)
    xlsx = openpyxl.load_workbook(filename=xlsx_io)
    xlsx_sheet = xlsx.active
    xlsx_data = xlsx_sheet.rows
    csv_string = ''

    for row in xlsx_data:
        l = list(row)
        
        for i in range(len(l)):
            if i == len(l) - 1:
                if l[i].value == None:
                    csv_string+=''
                else:
                    csv_string+=str(l[i].value)
            else:
                if l[i].value == None:
                    csv_string+=','
                else:
                    csv_string+=str(l[i].value) + ','
                
        csv_string+='\n'
    
    csv_string = StringIO(csv_string)
    csv_reader = csv.DictReader(csv_string)

    return csv_reader


def read_csv_reader(csv_reader):
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
