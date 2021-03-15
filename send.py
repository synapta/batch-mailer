import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
Prepare and send all mails
"""

# TODO: make test with next cloud
# TODO: remove the attachments

def send_mails(mails_dict):
    # Request parameters
    sender = 'giuseppe@synapta.it'
    password = ''
    port = 465  # For SSL
    smtp_server = 'smtp.gmail.com'

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        mails = prepare_mails(sender, mails_dict)
        for m in mails:
            server.sendmail(sender, m['recipient'], m['message'])


def prepare_mails(sender, mails_dict):
    mails = []
    # Prepare messages
    for md in mails_dict:
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = md['recipient']
        message["Subject"] = md['subject']
        message["Bcc"] = sender  # Recommended for mass emails
        
        # Add body to email
        body = md['body']
        message.attach(MIMEText(body, "plain"))

        # Add attached files
        attachments = md['attachments']
        parts = prepare_attachments(attachments)

        for p in parts:
            message.attach(p)
        
        message = message.as_string()
        recipient = md['recipient']
        mail = {}
        mail['message'] = message
        mail['recipient'] = recipient
        mails.append(mail)
    
    return mails


def prepare_attachments(attachments):
    parts = []

    for file_name in attachments:
        with open(file_name, "rb") as attached_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attached_file.read())

        # Encode file in ASCII characters to send by email    
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {file_name}",
        )

        parts.append(part)
    
    return parts
