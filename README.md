# batch-mailer
This tool allows users to send multiple mails, combining a template file (.docx) and a sheet file (.csv or .xlsx) to fill the template. Therefore, in order to use the tool, you have to prepare two different files:

* a .docx file. which includes variables in the form of `${variable}`;
* a .xlsx (or .csv) file, which includes fields corresponding to the .docx variables.

*WARNING: you have to remove all the double quotes in the xlsx file*. 

Moreover, the .xlsx files requires two mandatory fields:
* `oggetto`: it includes the string for the email subject;
* `pec`: it includes a vaild email address;

The .xlsx file can also include attachment fields in the form of `allegato1`, `allegato2`, `allegaton`. Valid links into these fields will be downloaded and attached to the email.  

## Install
Install virtualenv tool to create new virtual envs:

```
pip3 install virtualenv
```

Create the environment and install from requirements.txt:

```
cd batch-mailer
virtualenv -p python3.6 venv36
source venv36/bin/activate
pip3 install -r requirements.txt
```

In order to use the batch-mailer tool as desktop application, we need to install the python 3.6 version. This version is required by the [cefpython tool](https://github.com/cztomczak/cefpython), an open source project to provide Python bindings for the Chromium Embedded Framework (CEF). 

The Chromium project focuses mainly on Google Chrome application development, while CEF focuses on facilitating embedded browser use cases in third-party applications.

The cefpython tool in Ubuntu requires to install python as library. Therefore, you have to run the following command

```
sudo apt-get install libpython3.6-dev
```

## Local test
In order to test the desktop app, you can run the following command:

```
python main.py
```

A CEF window is opened and you can start to interact with the application.


Alternatively, you can open your browser at: http://localhost:8000/login.

## EXE generation
In order to run the application on Windows machines, you can generate an exe file using wine. You need to install the python 3.6 version for Windows and all the external libraries specified in `requirements.txt`.

Moreover, you need to install the [Pyinstaller tool](https://pypi.org/project/pyinstaller/), which is necessary to generate the .exe file.

This repository provides a `main.spec` file and a `hook-cefpython3.py` file in the `hooks` folder that specify all the dependencies (and the related paths) to build the .exe file. In particular, they provide all the instructions to use the uvicorn application server the cef tool in a Windows desktop app.

To generate the .exe, you can run the following command (in your .spec file you have to update the following lines related to the folder structure):

```
pathex=['C:\\Users\\Giuseppe\\Scrivania\\batch-mailer'],
        datas=[('C:\\Users\\Giuseppe\\Scrivania\\batch-mailer\\app', '.\\app')],
```

```
wine pyinstaller --onefile --clean main.spec
```

The .exe will be created in the `dist` folder. To test the Windows application in you Linux environment, you can run the followinc command:

```
cd dist
wine main.exe
```
