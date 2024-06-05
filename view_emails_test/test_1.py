from imapclient import IMAPClient
import logging
import ssl
import quopri
from dotenv import load_dotenv
import os

host = 'imap.gmail.com'
user =  "tjark.jakob.de@gmail.com"
password =  "sfwu cbae cfqy tjoj"

MAILSEARCH = "tjark.schulte@gy-cfg.de"
FOLDER = "INBOX"

context1 = []

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


        messages = server.search(['FROM', MAILSEARCH])


        for msgid, data in server.fetch(messages, ['ENVELOPE']).items():
            envelope = data[b'ENVELOPE']
            
            #add info to list
            
            msgid = {
                "id": msgid,
                "date": envelope.date,
                "subject": envelope.subject.decode(),
            }
            
            context1.append(msgid)
            
            
        # Nachrichten abrufen (inklusive BODY[TEXT])
        response = server.fetch(messages, ['BODY[TEXT]'])

        # Nachrichten durchgehen und anzeigen
        for msgid, data in response.items():
            # Entschlüssle den Text aus den Bytes
            decoded_text = quopri.decodestring(data[b'BODY[TEXT]']).decode('utf-8')

            # Zeige den entschlüsselten Text an
            for dict in context1:
                if dict.get("id") == msgid:
                    dict["content"] = decoded_text
                    
                

        context = {
            'emails': context1
        }
        

except Exception as e:
    print(f"Error: {e}")
