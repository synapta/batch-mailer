import inspect
import os
import sys
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import read
import check
import create
import send

csv = read.read_csv('test.csv')
doc = read.read_docx('test.docx')

res = check.validity(csv, doc)

print(res)

if res == 'OK':
    mails_dict = create.mails(csv, doc)
    #send.prepare_mails('giuseppe@synapta.it', mails)
    send.send_mails(mails_dict)
