from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import check
import read

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
async def load_files(request: Request, docx_file: UploadFile = File(...), xlsx_file: UploadFile = File(...)):
    docx = await docx_file.read()
    xlsx = await xlsx_file.read()
    res = process_inputs(xlsx, docx)
    return templates.TemplateResponse('index.html', context={'request': request})

# Preview

# Send

# Log page

def process_inputs(xlsx_byte, docx_byte):
    xlsx = read.read_csv(xlsx_byte)
    docx = read.read_docx(docx_byte)
    res = check.validity(xlsx, docx)

    return res