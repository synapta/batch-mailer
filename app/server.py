from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import re

import read
import check
import data
import create
import send

# Prepare fastAPI
base_dir = os.path.dirname(os.path.abspath(__file__)) # Get the path files: useful to import static and templates
app = FastAPI()
app.mount('/static', StaticFiles(directory=os.path.join(base_dir, 'static')), name='static')
templates = Jinja2Templates(directory=os.path.join(base_dir, 'templates'))

# Login
@app.get('/login')
def login(request: Request):
    return templates.TemplateResponse('login.html', context={'request': request})

# Check login
@app.post('/login')
def check_login(request: Request,
                sender: str = Form(...),
                password: str = Form(...),
                server: str = Form(...),
                port: int = Form(...)):
    
    result, _ = check.valid_login_connection(sender, password, server, port)

    if result == 'OK':
        data.mail_login['sender'] = sender
        data.mail_login['password'] = password
        data.mail_login['server'] = server
        data.mail_login['port'] = port
    
    return result


# Home
@app.get('/index')
def home(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})


# Check
@app.post('/index')
async def load_files(request: Request,
                     docx_file: UploadFile = File(...),
                     xlsx_file: UploadFile = File(...)):
    
    docx_byte = await docx_file.read()
    xlsx_byte = await xlsx_file.read()

    # Store file metadata
    data.docx['name'] = docx_file.filename
    data.docx['content-type'] = 'docx'
    data.xlsx['name'] = xlsx_file.filename
    data.xlsx['content-type'] = re.search("(?:\.([^.]+))?$", xlsx_file.filename).group(1).replace('.','')

    # Process and manage the results
    result, docx, xlsx = await process_inputs(xlsx_byte, data.xlsx['content-type'], docx_byte)

    if result == 'OK':
        data.mails = create.mails(xlsx, docx)
        data.docx['file'] = docx
        data.xlsx['file'] = xlsx

    return result


# Preview
@app.get('/preview')
def prepare_preview(request: Request):
    context = {
        'request': request,
        'subject': data.mails[0]['subject'],
        'recipient' : data.mails[0]['recipient'],
        'body': data.mails[0]['body'],
        'attachments': data.mails[0]['attachments'],
        'num_recipients': len(data.mails),
        'recipients': [ i['recipient'] for i in data.mails],
        'docx_template': data.docx['name']
    }

    return templates.TemplateResponse('preview.html', context=context)


# Send
@app.get('/send')
async def massive_send(request: Request):
    msg, mails_sent = await send.send_mails(data.mails)
    mails_ok = 0

    for i in mails_sent:
        if i['response'] == 'OK':
            mails_ok+=1

    context = {
        'request': request,
        'mails': mails_sent,
        'num_true': mails_ok,
        'num_all' : len(mails_sent)
    }
    
    return templates.TemplateResponse('results.html', context=context)


async def process_inputs(xlsx_byte, xlsx_content_type, docx_byte):
    csv_reader = None
    
    if xlsx_content_type == 'csv':
        csv_reader = read.read_csv(xlsx_byte)
    elif xlsx_content_type == 'xlsx':
        csv_reader = read.read_xlsx(xlsx_byte)
    
    xlsx = read.read_csv_reader(csv_reader)
    docx = read.read_docx(docx_byte)
    res = await check.validity(xlsx, docx)

    return res, docx, xlsx
