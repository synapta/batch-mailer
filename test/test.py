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

mails_dict = [{'subject': 'Oggetto della mail per Caruso', 'recipient': 'giuseppe.futia@gmail.com', 'body': 'Gentile Caruso,\n\nLe scrivo questa brevissima mail di test per il progetto Progetto di Caruso.\n\nWikimedia Italia', 'attachments':[]}]
send.send_mails(mails_dict)
