__author__ = 'Sebastian.Law'

import os
import email
import html2text

def extract_body(message):
    assert type(message) == email.message.Message
    content = None
    # stage = None
    if type(message.get_payload()) is str:
        if message.get_content_type() == 'text/plain':
            content = message.get_payload(decode=True).decode(message.get_content_charset())
            # stage = 1
        elif message.get_content_type() == 'text/html':
            content = message.get_payload(decode=True).decode(message.get_content_charset())
            content = html2text.html2text(content).replace("|", "").replace("---", "")
            # stage = 2
        else:
            print(os.path.basename(__file__), "ERROR")
    else:
        for part in message.get_payload():
            if part.get_content_type() == 'text/plain':
                # stage = 4
                content = part.get_payload(decode=True).decode(part.get_content_charset())
                break
        if content is None:  # no plain text found, may be nested in multipart
            for part in message.get_payload():
                if part.get_content_type() == 'multipart/alternative':
                    for subpart in part.get_payload():
                        if subpart.get_content_type() == 'text/plain':
                            # stage = 5
                            content = subpart.get_payload(decode=True).decode(subpart.get_content_charset())
                            break
                    if content is not None:
                        break
    return content
