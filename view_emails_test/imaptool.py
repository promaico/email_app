import logging
import ssl
from imapclient import IMAPClient
import quopri

HOST = "imap.1blu.de"
MAILADR = "stecknadel.im@fschulte.net"
USERNAME = "o265439_0-stecknadelim"
PASSWORD = "234234!34!"

MAILSEARCH = "fschulte.de@web.de"

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    level=logging.INFO
)

ssl_context = ssl.create_default_context()

# don't check if certificate hostname doesn't match target hostname
ssl_context.check_hostname = False

# don't check if the certificate is trusted by a certificate authority
ssl_context.verify_mode = ssl.CERT_NONE

with IMAPClient(HOST, ssl_context=ssl_context) as server:
    server.login(USERNAME, PASSWORD)
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
