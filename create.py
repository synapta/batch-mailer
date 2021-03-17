import re
from docx import Document

import os
from urllib.parse import urlparse


def mails(csv, templ):
    all_mails = []
    data = csv['data']

    for row in data:
        m = {}

        # Subject
        m['subject'] = row['oggetto'] 

        # Recipient
        m['recipient'] = row['pec']

        # Mail text
        doc = mail_text(row, templ)
        text_doc = get_text(doc)
        m['body'] = text_doc

        # Attachments
        m['attachments'] = []

        for k,v in row.items():
            if 'allegato' in k and v != '':
                url_text = urlparse(v)
                name = os.path.basename(url_text.path) 
                m['attachments'].append(name)

        all_mails.append(m)
    
    return all_mails


def mail_text(row, templ):
    doc = Document()
    pattern = '\$\{(.*?)\}'

    for p in templ.paragraphs:
        par_vars = re.findall(pattern, p.text)

        for v in par_vars:
            upd_p = p.text.replace('${' + v + '}', row[v])
            doc.add_paragraph(upd_p)
    
    return doc


def get_text(doc):
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    
    return '\n\n'.join(fullText)
