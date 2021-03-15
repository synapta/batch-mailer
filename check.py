import re
import read

import os
import requests
from urllib.parse import urlparse

"""
Consistency check in the files
"""

# TODO: verificare se occorrono ulteriori controlli sul testo, ad esempio strim()
# TODO: verificare se ci possono essere altri ricevitori e come possono farlo
# TODO: non processare file che sono già stati scaricati
# TODO: migliora la gestione degli attachments (sposterei tutti in utils)

def validity(csv, doc):
    # 'oggetto' and 'pec' are required
    if not valid_csv:
        return 'Controlla che i campi "oggetto" e "pec" siano presenti nel file excel'

    headers = csv['headers']
    data = csv['data']
    pattern = '\$\{(.*?)\}'

    doc_vars = []
    for p in doc.paragraphs:
        par_vars = re.findall(pattern, p.text)
        doc_vars.extend(par_vars)
    
    # the document requires at least one variable
    if len(doc_vars) == 0:
        return 'Attenzione: sembra che il template inserito non contenga nessuna variabile. La sintassi per inserirle è "$\{nome variabile\}"'
    
    # check consistency between the csv headers and the doc vars
    headers_vars = [v for v in headers if v != 'oggetto' and v != 'pec' and 'allegato' not in v]
    headers_vars.sort()
    doc_vars.sort()

    if headers_vars != doc_vars:
        # TODO: do they need further information?
        return 'Attenzione: i campi del file excel e del file .docx non sono allineati'
    
    # check and download the attachments
    line = 1
    attachments = {}
    for l in data:
        line_attachments = []
        for k,v in l.items():
            if 'allegato' in k:
                line_attachments.append(v)
        attachments[line] = line_attachments
        line+=1
    
    attach_errors = not_valid_attachments(attachments)

    if len(attach_errors) > 0:
        return attach_errors

    return 'OK'
    

def valid_csv(csv):
    headers = csv['headers']
    if 'oggetto' not in headers or 'pec' not in headers:
        return False
    
    return True


def not_valid_attachments(attachments):
    """
    Check and download the attachments if valid
    """

    errors = []

    for k,v in attachments.items():
        urls = [u for u in v if 'http://' in u or 'https://' in u]

        print(urls)

        for url in urls:
            url_text = urlparse(url)
            name = os.path.basename(url_text.path) 
            r = requests.get(url, allow_redirects=True)
            if len(url) > 0 and name == '':
                errors.append("""Controlla l\'allegato {u} alla riga {k}. Non sembra un file valido.""".format(u=url, k=k))
            else:
                open(name, 'wb').write(r.content)

    return errors