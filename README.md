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