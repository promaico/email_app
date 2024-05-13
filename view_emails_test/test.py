from imapclient import IMAPClient
import email
import logging
import ssl
import quopri 
from dotenv import load_dotenv
import os
load_dotenv()


mail = os.environ.get("MAIL")
mail_pass = os.environ.get("PASS")


host = 'imap.gmail.com' 
user = mail 
password = mail_pass 


MAILSEARCH = "tjark.schulte@gy-cfg.de"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.INFO
)

ssl_context = ssl.create_default_context()


ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

with IMAPClient(host, ssl_context=ssl_context) as server:
    server.login(user, password)
    select_info = server.select_folder('INBOX')
    print('%d messages in INBOX' % select_info[b'EXISTS'])

    messages = server.search(['FROM', MAILSEARCH])
    print("%d messages from our best friend" % len(messages))

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
        print(f"Nachricht {msgid}:")
        print(f"Inhalt:\n{decoded_text}\n")


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
