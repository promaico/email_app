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

MAILSEARCH = "tjark.schulte@gy-cfg.de"
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
        print(f'%d Nachrichten in {FOLDER.lower().capitalize()}' % select_info[b'EXISTS'])
        print("\n")

        messages = server.search(['FROM', MAILSEARCH])
        print(f"%d Nachrichten von {MAILSEARCH}" % len(messages))
        print("\n")

        for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
            envelope = data[b'ENVELOPE']
            print('ID #%d: "%s" received %s' % (msgid, envelope.subject.decode(), envelope.date))

        # Nachrichten abrufen (inklusive BODY[TEXT])
        response = server.fetch(messages, ['BODY[TEXT]'])

        # Nachrichten durchgehen und anzeigen
        for msgid, data in response.items():
            # Entschlüssle den Text aus den Bytes
            decoded_text = quopri.decodestring(data[b'BODY[TEXT]']).decode('utf-8')

            # Zeige den entschlüsselten Text an
            print(f"Betreff: \t{envelope.subject.decode()}")
            print(f"Inhalt: \t{decoded_text}\n")

        # Start IDLE mode
        server.idle()
        print("Connection is now in IDLE mode, send yourself an email or quit with ^c")

        while True:
            try:
                # Wait for up to 30 seconds for an IDLE response
                responses = server.idle_check(timeout=30)
                print("Server sent:", responses if responses else "nothing")
            except KeyboardInterrupt:
                break

        server.idle_done()
        print("\nIDLE mode done")
except Exception as e:
    print(f"Error: {e}")
