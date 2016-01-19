__author__ = 'Sebastian.Law'

import os
import datetime

# import files
# import main
# import vendors
#
# pickle_folder = os.path.join(files.local_path, 'pickles')
# # pickle_names
# # for root, directories, file_names in os.walk(pickle_folder):
# #     for f in file_names:
# file_names = os.listdir(pickle_folder)
# pickle_names = [os.path.join(files.local_path, 'pickles', f) for f in file_names]
# all_data = [main.load_pickle(p) for p in pickle_names]
#
# vens = vendors.load_vendors()
# data = {}
# for v in vens:
#     data.update({v.get_id(): None})

filename = os.path.join(os.path.expanduser('~'), 'Google Drive', 'Rial Corporate Dev', 'workings', 'output.txt')
print(filename)
with open(filename, 'a') as f:
    f.write(str(datetime.datetime.now())+"\n")



# import os
# import files
# import smtplib
# import email

# sender = 'realcorporate@sebastianhlaw.com'
# recipient = 'sebastian.law@duffandphelps.com'
# password_file = open(files.sebastianhlaw_password_file, 'r')
# password = password_file.read()
# password_file.close()

# Create the message
# msg = email.mime.text.MIMEText('This is the body of the message.')
# msg['To'] = email.utils.formataddr(('Recipient', recipient))
# msg['From'] = email.utils.formataddr(('Sebastian Law (realcorporate)', sender))
# msg['Subject'] = 'Automated update email'

# msg = email.mime.multipart.MIMEMultipart(From=sender, To=recipient, Subject="Automated sales update")
# msg.attach(email.mime.text.MIMEText("Update details"))
# with open(files.output_logger, "rb") as f:
#     msg.attach(email.mime.application.MIMEApplication(
#         f.read(),
#         Content_Disposition='attachment; filename="%s"' % os.path.basename(f),
#         Name=os.path.basename(f)
#     ))


# server = smtplib.SMTP('smtp.ipage.com')
# server.set_debuglevel(True)  # show communication with the server
# try:
#     server.ehlo()  # identify ourselves, prompting server for supported features
#     if server.has_extn('STARTTLS'):  # If we can encrypt this session, do it
#         server.starttls()
#         server.ehlo()  # re-identify ourselves over TLS connection
#     server.login(sender, password)
#     server.sendmail(sender, [recipient], msg.as_string())
# finally:
#     server.quit()