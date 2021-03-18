from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import check
import read
import create

# Data Models
class Preview(BaseModel):
    subject: str
    recipient: str
    body: str
    lines : int

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

    # Process and manage the results
    result, docx, xlsx = process_inputs(xlsx_byte, docx_byte)

    print('Processing output:')
    print(result)

    if result == 'OK':
        mails = create.mails(xlsx, docx)
        subject = mails[0]['subject']
        recipient = mails[0]['recipient']
        body = mails[0]['body']
        response = {}
        response['field'] = 'OK'
        data = {
            'subject': subject,
            'recipient': recipient,
            'body': body,
            'lines': len(mails),
            'mails': mails  
        }
        response['data'] = data
        
        return response
    
    return result


# Preview
@app.post('/preview')
async def prepare_preview(request: Request, preview:Preview):
    preview = preview.dict()
    context = {
            'request': request,
            'subject': preview['subject'],
            'recipient' : preview['recipient'],
            'body': preview['body']
    }
    return templates.TemplateResponse('preview.html', context=context)


# TODO SEND


def process_inputs(xlsx_byte, docx_byte):
    xlsx = read.read_csv(xlsx_byte)
    docx = read.read_docx(docx_byte)
    res = check.validity(xlsx, docx)

    return res, docx, xlsx
