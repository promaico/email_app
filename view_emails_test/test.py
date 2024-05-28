from imapclient import IMAPClient
import logging
import ssl
import quopri
from dotenv import load_dotenv
import os

load_dotenv()

host = 'imap.gmail.com'
user = os.environ.get("MAIL")
password = os.environ.get("PASS")

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

            print(f"Datum: {envelope.date}")
            print(f"Betreff: {decoded_subject}")
            print(f"Inhalt: {decoded_text}\n")

except Exception as e:
    print(f"Fehler: {e}")
