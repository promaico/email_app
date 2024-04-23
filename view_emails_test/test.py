import imaplib
import email
from email.header import decode_header
import datetime

# Ihre Anmeldeinformationen
username = 'tjark.jakob.de@gmail.com'
password = 'hsmd eayd sssh rfgn'
imap_url = 'imap.gmail.com'

# Verbindung zum Server herstellen
mail = imaplib.IMAP4_SSL(imap_url)

# Anmelden
mail.login(username, password)

# Wählen Sie den Posteingang aus, den Sie durchsuchen möchten
mail.select("inbox")

# Suchen Sie alle E-Mails
result, data = mail.uid('search', None, "ALL")

# Erhalten Sie die Liste der E-Mail-IDs
email_ids = data[0].split()
latest_10_email_ids = email_ids[-10:]

for id in latest_10_email_ids:
    result, email_data = mail.uid('fetch', id, '(BODY.PEEK[HEADER])')
    raw_email = email_data[0][1].decode("utf-8")
    email_message = email.message_from_string(raw_email)

    # Header-Details
    date_tuple = email.utils.parsedate_tz(email_message['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
        local_message_date = "%s" %(str(local_date.strftime("%a, %d %b %Y %H:%M:%S")))
    email_from = str(decode_header(email_message['From'])[0][0])
    email_to = str(decode_header(email_message['To'])[0][0])
    subject = str(decode_header(email_message['Subject'])[0][0])

    print('Von : ' + email_from + '\n')
    print('An : ' + email_to + '\n')
    print('Betreff : ' + subject + '\n')
    print('Datum : ' + local_message_date + '\n')
