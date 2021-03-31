import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import socket
import os

import check
import data
import utils

'''
Prepare and send all mails
'''

async def send_mails(mails_dict):
    print('\nSending emails')
    
    # Request parameters
    sender = data.mail_login['sender']
    password = data.mail_login['password']
    port = data.mail_login['port'] # 465 For SSL
    server = data.mail_login['server']
    msg = ''
    mails_sent = []

    logged, smtp_server = check.valid_login_connection(sender, password, server, port)
    
    # Massive mail sending
    if logged == 'OK':
        mails = await prepare_mails(sender, mails_dict)
        for m in mails: 
            res = send_single_mail(smtp_server, sender, m['recipient'], m['message'])
            mr = {'recipient': m['recipient'],
                  'response': res}
            mails_sent.append(mr)
        
        # Quit
        smtp_server.quit()

        # Remove all downloaded attachments
        for md in mails_dict:
            urls = md['attachments']
            for url in urls:
                file_name = utils.get_name_from_url(url)
                if os.path.exists(file_name):
                    os.remove(file_name)
    
    print('    %s' % msg)

    return msg, mails_sent


async def prepare_mails(sender, mails_dict):
    mails = []
    # Prepare messages
    for md in mails_dict:
        message = MIMEMultipart()
        message['From'] = sender
        message['To'] = md['recipient']
        message['Subject'] = md['subject']
        
        # Add body to email
        body = md['body']
        message.attach(MIMEText(body, 'plain'))

        # Add attached files
        attachments = md['attachments']
        parts = await prepare_attachments(attachments)

        for p in parts:
            message.attach(p)
        
        message = message.as_string()
        recipient = md['recipient']
        mail = {}
        mail['message'] = message
        mail['recipient'] = recipient
        mails.append(mail)
    
    return mails


async def prepare_attachments(urls):
    parts = []
    file_names = []
    
    # Process results
    results = await utils.multi_requests(urls, utils.request)
    for i in results:
        file_name = i['file_name']
        response = i['response']
        if response == 200:
            file_names.append(file_name)

    for file_name in file_names:
        with open(file_name, 'rb') as attached_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attached_file.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {file_name}',
        )

        parts.append(part)
    
    return parts


def send_single_mail(server, sender, recipient, message):
    msg = 'OK'
    try:
        server.sendmail(sender, recipient, message)
    except smtplib.SMTPSenderRefused as sender_refused:
        msg = 'Invio mail - Indirizzo del mittente rifiutato: %s' % sender
        print(sender_refused)
    except smtplib.SMTPRecipientsRefused as recipient_refused:
        msg = 'Invio mail - Indirizzo del destinatario rifiutato: %s' % recipient
        print(recipient_refused)
    except smtplib.SMTPDataError as data_err:
        msg = 'Invio mail - Messaggio non accettato dal server di posta: %s' % str(message)
        print(data_err)
    except smtplib.SMTPException as smtp_err:
        msg = 'Invio mail - Errore generico di SMTP'
        print(smtp_err)
    except Exception as err:
        msg = 'Invio mail - Errore generico'
        print(err)
    
    return msg