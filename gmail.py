__author__ = 'Sebastian.Law'

# TODO: deal with when there are 0 emails to pull

import imaplib
import getpass
import os
import email
import html2text
import files
import datetime


def connect(default=True):
    connection = imaplib.IMAP4_SSL('imap.gmail.com')
    username = 'gixtix.sales@gmail.com'
    if default is True:
        password_file = open(files.password_file, 'r')
        password = password_file.read()
        password_file.close()
    else:
        password = getpass.getpass()
    connection.login(username, password)
    return connection


def get_messages(connection, folder, read_only=True, *args):
    # imap.list()  # lists the items in the mailbox parent
    typ, mailbox = connection.select(folder, readonly=read_only)
    typ, data = connection.uid("SEARCH", *args)
    # *search, contains list of items e.g. "(UNSEEN)", "(SINCE 10-Oct-2015)"
    # date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
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
        if content is None:  # no plain text found, may be nested in multipart
            for part in message.get_payload():
                if part.get_content_type() == 'multipart/alternative':
                    for subpart in part.get_payload():
                        if subpart.get_content_type() == 'text/plain':
                            content = subpart.get_payload(decode=True).decode(subpart.get_content_charset())
                            break
                    if content is not None:
                        break
    date_tuple = email.utils.parsedate_tz(message['Date'])
    local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
    return local_date, content


def get_message_contents(folder, read_only=True, *args):
    connection = connect()
    messages = get_messages(connection, folder, read_only, *args)
    connection.logout()
    if messages:
        contents = [extract_message_content(m) for m in messages]
        print(folder, "processed,", len(contents), "messages pulled.")
        return contents
    else:
        print(folder, "processed, no messages to pull.")


