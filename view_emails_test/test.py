from imapclient import IMAPClient
import email
import quopri  # Importiere das quopri-Modul


# Verbindungsinformationen
host = 'imap.gmail.com'  # Dein IMAP-Server
user = 'tjark.jakob.de@gmail.com'  # Deine E-Mail-Adresse
password = 'ahcl hyql elqc ratb'  # Dein Passwort
ssl = True  # SSL verwenden (True oder False)


# Verbindung zum IMAP-Server herstellen
server = IMAPClient(host, use_uid=True, ssl=ssl)
server.login(user, password)

# Den "gelesen" Ordner auswählen
inboxInfo = server.select_folder('INBOX')

# Die letzten 10 Nachrichten suchen (nicht gelöscht)
messages = server.search(['FROM', 'tjark.schulte@gy-cfg.de'])

# Nachrichten abrufen (inklusive BODY[TEXT])
response = server.fetch(messages, ['BODY[TEXT]'])

# Nachrichten durchgehen und anzeigen
for msgid, data in response.items():
    # Entschlüssle den Text aus den Bytes
    decoded_text = quopri.decodestring(data[b'BODY[TEXT]']).decode('utf-8')

    # Zeige den entschlüsselten Text an
    print(f"Nachricht {msgid}:")
    print(f"Inhalt:\n{decoded_text}\n")

# Verbindung schließen
server.logout()

