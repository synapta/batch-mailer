from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import data
import check
import read
import create
import send

# Prepare fastAPI
app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='./')

# Home
@app.get('/')
def home(request: Request):
    return templates.TemplateResponse('index.html', context={'request': request})

# Check
@app.post('/')
async def load_files(request: Request,
                     docx_file: UploadFile = File(...),
                     xlsx_file: UploadFile = File(...)):
    
    docx_byte = await docx_file.read()
    xlsx_byte = await xlsx_file.read()

    # Store file metadata
    data.docx['name'] = docx_file.filename
    data.docx['content-type'] = docx_file.content_type
    data.xlsx['name'] = xlsx_file.filename
    data.xlsx['content-type'] = xlsx_file.content_type

    # Process and manage the results
    result, docx, xlsx = process_inputs(xlsx_byte, docx_byte)

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
        'body': data.mails[0]['body']
    }

    return templates.TemplateResponse('preview.html', context=context)


# Send
@app.get('/send')
async def massive_send(request: Request):
    context = {
        'request': request
    }
    send.send_mails(data.mails)
    print('Return after processing')
    
    return templates.TemplateResponse('results.html', context=context)


def process_inputs(xlsx_byte, docx_byte):
    xlsx = read.read_csv(xlsx_byte)
    docx = read.read_docx(docx_byte)
    res = check.validity(xlsx, docx)

    return res, docx, xlsx
