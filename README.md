# README - email_app

Creating an Webapp for managing (multiple) e-mails on one account. Currently using Python/Django/HTML/CSS.

# setup

```
git clone https://github.com/promaico/email_app.git

# virtual env setup (one time after each git clone to empty folder)
python  -m venv email_app/.venv

cd email_app

# activate env setup
. ./.venv/Scripts/activate

# install dependencies
pip install -r requirements.txt
```

# run test code for imap4 handling outside from django

```
cd view_emails_test
python imaptool.py
```

# update changed dependencies at times

```
pip freeze > requirements.txt
```


END.
