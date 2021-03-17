import re
import read

import os
import requests
from urllib.parse import urlparse

"""
Consistency check in the files
"""

# TODO: verificare se occorrono ulteriori controlli sul testo, ad esempio strim()
# TODO: migliora la gestione degli attachments

def validity(csv, doc):

    # 'oggetto' and 'pec' are required
    valid, msg = valid_csv(csv)
    if not valid:
        print(msg['text'])
        return msg
    
    # check consistency between the csv headers and the doc vars
    valid, msg = valid_consistency(csv, doc)
    if not valid:
        print(msg['text_docx'])
        print(msg['text_xlsx'])
        return msg
    
    # check and download the attachments
    valid, msg = valid_attachments(csv)
    if not valid:
        print(msg['text'])
        return msg

    return 'OK'
    

def valid_csv(csv):
    print('\nCheck csv fields (oggetto and pec are required)')
    msg = {}
    valid = True
    
    headers = csv['headers']
    if 'oggetto' not in headers or 'pec' not in headers:
        valid = False
        msg['field'] = 'xlsx'
        msg['text'] = 'Controlla che i campi "oggetto" e "pec" siano presenti nel file excel'
    
    return valid, msg


def valid_consistency(csv, doc):
    print('\nCheck the consistency between the .docx and the .xlsx or .csv')
    msg = {}
    valid = True

    # Get the .docx vars
    pattern = '\$\{(.*?)\}'
    doc_vars = []
    for p in doc.paragraphs:
        par_vars = re.findall(pattern, p.text)
        doc_vars.extend(par_vars)

    # Get .csv or .xlsx vars
    headers = csv['headers']
    headers_vars = [v for v in headers if v != 'oggetto' and v != 'pec' and 'allegato' not in v]

    # Check consistency
    doc_vars.sort()
    headers_vars.sort()

    if doc_vars != headers_vars:
        valid = False
        join_str = ', '
        msg['field'] = 'both'
        msg['text_docx'] = 'Attenzione i campi del .docx sono: [' + join_str.join(doc_vars) + ']. ' 
        msg['text_xlsx'] = 'Attenzione i campi del .xlsx o .csv sono [' + join_str.join(headers_vars) + '] .'
    
    return valid, msg


def valid_attachments(csv):
    print('\nCheck if the attachments are valid')
    msg = {}
    valid = True

    # Get all the attachments
    data = csv['data']
    line = 1
    attachments = {}
    for l in data:
        line_attachments = []
        for k,v in l.items():
            if 'allegato' in k:
                line_attachments.append(v)
        attachments[line] = line_attachments
        line+=1
    
    # Check and download all the attachments
    text_error = ''
    for k, v in attachments.items():
        urls = [u for u in v if 'http://' in u or 'https://' in u]
        for url in urls:
            url_text = urlparse(url)
            name = os.path.basename(url_text.path)
            
            # Won't be able to identify the name file
            if len(url) > 0 and name == '':
                valid = False
                mgs['field'] = 'xlsx'
                text_error += """Controlla l\'allegato {u} alla riga {k}. Non sembra un file valido.\n""".format(u=url, k=k)
                msg['text'] = text_error
    
    return valid, msg
