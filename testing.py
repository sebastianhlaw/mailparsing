
import main
import files
import os


def lazy_load(jar="test-2016-02-18-14-12-10"):
    file_name = os.path.join(files.pickle_folder, jar + ".pkl")
    return main.load_minimal_messages(file_name)


def lazy_pull(search="(SINCE 12-Feb-2016)"):
    return main.get_minimal_messages("INBOX", True, search)


def lazy_extract(mm, i=0, debug=True):
    return main.extract_single(mm[i], debug)


def lazy_display(mm, i=0, file=None):
    if file:
        file_name = os.path.join(files.testing_folder, str(file)+".txt")
        with open(file_name, 'w') as f:
            f.write("SUBJECT:\t"+mm[i].subject+"\n")
            f.write("SENT_TIME:\t"+str(mm[i].sent_time)+"\n")
            f.write("VENDOR_ID:\t"+mm[i].vendor+"\n")
            f.write("CONTENT:\n"+mm[i].content+"\n")
    else:
        print("SUBJECT:\t", mm[i].subject)
        print("SENT_TIME:\t", str(mm[i].sent_time))
        print("VENDOR_ID:\t", mm[i].vendor)
        print("CONTENT:\n", mm[i].content)


def lazy_search(mm, string):
    for i, m in enumerate(mm):
        if string in m.content:
            print(i)


# def extract_n(i, debug=True):
#     return main.extract_email(data, vens, v, i, debug)
#
#
# def display_n(i, save=False):
#     main.display_email(data, vens, v, i, save)
#
#
# def search(date):  # this probably won't work now I changed date methodology
#     main.find_mail(data, vens, date)
#
#
# def run():
#
#     t = main.extract_all(data, vens)
#     main.dump_data(t, files.output_test, True)
