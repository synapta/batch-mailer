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

    # Process and manage the results
    res = process_inputs(xlsx, docx)

    if res == 'OK':
        return templates.TemplateResponse('preview.html', context={'request': request})

    if res['field'] == 'xlsx':
        result_docx = ''
        result_xlsx = res['text']
        return templates.TemplateResponse('index.html', context={'request': request, 'result_docx': result_docx, 'result_xlsx': result_xlsx})
    
    if res['field'] == 'both':
        result_docx = res['text_docx']
        result_xlsx = res['text_xlsx']
        return templates.TemplateResponse('index.html', context={'request': request, 'result_docx': result_docx, 'result_xlsx': result_xlsx})    


# TODO SEND


def process_inputs(xlsx_byte, docx_byte):
    xlsx = read.read_csv(xlsx_byte)
    docx = read.read_docx(docx_byte)
    res = check.validity(xlsx, docx)

    return res