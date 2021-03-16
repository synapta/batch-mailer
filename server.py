from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
async def load_files(request: Request, docx_file: UploadFile = File(...)):
    docx = await docx_file.read()
    return templates.TemplateResponse('index.html', context={'request': request})

# Preview

# Send

# Log page