import re
import aiohttp

import read
import utils

"""
Consistency check in the files
"""

# TODO: verificare se occorrono ulteriori controlli sul testo, ad esempio strim()

async def validity(csv, doc):

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
    valid, msg = await valid_attachments(csv)
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


async def valid_attachments(csv):
    print('\nCheck if the attachments are valid')
    msg = {}
    msg['text'] = ''
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
    
    # Check all the attachments
    for row, urls in attachments.items():
        
        # No empty 'allegato' fields
        valid_urls = [i.strip() for i in urls if i.strip() != '']
        
        # Get headers (async way) and process
        results = await utils.multi_requests(valid_urls, utils.request_header)
        for r in results:
            if type(r['response']) == dict:
                url = r['url']
                ct = r['response']['content-type'].lower()
                if 'text' in ct or 'html' in ct:
                    valid = False
                    msg['field'] = 'xlsx'
                    msg['text'] += """Controlla l\'allegato {u} alla riga {r}. Il link non contiene un file.\n""".format(u=url, r=int(row)+1)
            else:
                url = r['url']
                valid = False
                msg['field'] = 'xlsx'
                msg['text'] += """Controlla l\'allegato {u} alla riga {r}. Non sembra un link valido.\n""".format(u=url, r=int(row)+1)
    
    return valid, msg
