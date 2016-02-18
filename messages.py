
import imaplib
import os
import email
import files
import datetime
import html2text


def connect(username_file="main_username.txt", password_file="main_password.txt"):
    connection = imaplib.IMAP4_SSL('imap.ipage.com')
    with open(os.path.join(files.local_path, 'private', username_file), 'r') as file:
        username = file.readline()
    with open(os.path.join(files.local_path, 'private', password_file), 'r') as file:
        password = file.readline()
    connection.login(username, password)
    return connection


def get_messages(connection, folder="INBOX", read_only=True, *args):
    typ, mailbox = connection.select(folder, readonly=read_only)
    if not args:  # *args e.g. "(UNSEEN)", "(SINCE 10-Oct-2015)"
        default_search_date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
        typ, data = connection.uid("SEARCH", "(SINCE "+default_search_date+")")
    else:
        typ, data = connection.uid("SEARCH", *args)
    uids = data[0].split()
    uids = [uid.decode("utf-8") for uid in uids]
    messages = []
    for uid in uids:
        typ, data = connection.uid('FETCH', uid + ' (RFC822)')
        for part in data:
            if isinstance(part, tuple):
                messages.append(email.message_from_bytes(part[1]))
    connection.close()
    return messages


def mail_type_from_subject(subject):
    assert type(subject) == str
    text = subject.lower()
    if "pending" in text or "provisional" in text:
        return "PENDING"
    elif "sale" in text or "sold" in text:
        return "SALE"


def vendor_from_subject(subject):
    assert type(subject) == str
    text = subject.lower()
    vendor = None
    if "get me in" in text:
        vendor = "GMI"
    elif "seatwave" in text:
        vendor = "SEAT"
    return vendor


def vendor_from_message_content(content):
    assert type(content) == str
    text = content.lower()
    vendor = None
    if "stubhub.co.uk" in text:
        vendor = "STUB"
    elif "getmein.com" in text:
        vendor = "GMI"
    elif "viagogo.com" in text:
        vendor = "VIA"
    elif "seatwave.com" in text:
        vendor = "SEAT"
    return vendor


def extract_message_sent_time(message):
    assert type(message) == email.message.Message
    if message['Date']:
        date_tuple = email.utils.parsedate_tz(message['Date'])
        return datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))


def extract_message_content(message):
    assert type(message) == email.message.Message
    content = None
    if type(message.get_payload()) is str:
        if message.get_content_type() == 'text/plain':
            content = message.get_payload(decode=True).decode(message.get_content_charset())
        elif message.get_content_type() == 'text/html':
            content = message.get_payload(decode=True).decode(message.get_content_charset())
            content = html2text.html2text(content).replace("|", "").replace("---", "")
        else:
            print(os.path.basename(__file__), "ERROR")
    else:
        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                content = part.get_payload(decode=True).decode(part.get_content_charset())
                break
        if content is None:                                 # no plain text found, may be nested in multipart
            for part in message.get_payload():
                if part.get_content_type() == 'multipart/alternative':
                    for subpart in part.get_payload():
                        if subpart.get_content_type() == 'text/plain':
                            content = subpart.get_payload(decode=True).decode(subpart.get_content_charset())
                            break
                    if content is not None:
                        break
    return content


class MinimalMessage:
    def __init__(self, message=None):
        self.subject = None
        self.sent_time = None
        self.content = None
        self.mail_type = None
        self.vendor = None
        if message:
            self.extract_message(message)

    def extract_message(self, message):
        assert type(message) == email.message.Message
        self.subject = message['Subject']
        self.sent_time = extract_message_sent_time(message)
        self.content = extract_message_content(message)
        self.mail_type = mail_type_from_subject(self.subject)
        self.vendor = vendor_from_subject(self.subject)     # try to pull the vendor from the subject line
        if not self.vendor:                                 # otherwise pull it from the main message
            self.vendor = vendor_from_message_content(self.content)
        if not self.vendor:
            self.mail_type = "UNKNOWN"
