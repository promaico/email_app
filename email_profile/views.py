from django.shortcuts import render
from imapclient import IMAPClient
import logging
import ssl
import quopri
from dotenv import load_dotenv
import os
# Create your views here.


def profile(request):
    return render(request, "profile.html")


def profile_email(request):

    load_dotenv()

    host = 'imap.gmail.com'
    user = os.environ.get("MAIL")
    password = os.environ.get("PASS")
    
    email_subject = []
    email_content = []
    email_date = []

    FOLDER = "INBOX"

    logging.basicConfig(
        format='%(asctime)s - %(levelname)s: %(message)s',
        level=logging.INFO
    )

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    try:
        with IMAPClient(host, ssl_context=ssl_context) as server:
            server.login(user, password)
            select_info = server.select_folder(FOLDER)
            # Suche nach ungelesenen E-Mails
            messages = server.search(['SEEN'])

            # Begrenze die Anzahl der angezeigten E-Mails auf 10
            max_displayed_emails = 10
            for msg_id, data in server.fetch(messages[:max_displayed_emails], ['ENVELOPE', 'BODY[TEXT]']).items():
                envelope = data[b'ENVELOPE']
                decoded_text = quopri.decodestring(data[b'BODY[TEXT]']).decode('latin-1')  # Ändere die Codierung hier
                decoded_subject = envelope.subject.decode("utf-8")
                email_subject.append(decoded_subject)
                email_content.append(decoded_text)
                
    except Exception as e:
        print(f"Fehler: {e}")
        
        
    return render(request, "profile.html", email_subject, email_content)