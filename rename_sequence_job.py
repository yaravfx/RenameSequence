# :coding: utf-8
"""
    Rename sequence tool base function
"""


import re
import os
import shutil
from optparse import OptionParser



class renameSequence:
    def __init__(self, src_file, new_file, operation):
        self.srcFile = src_file
        self.srcSequenceName = os.path.splitext(os.path.basename(self.srcFile))[0]
        self.ext = os.path.splitext(src_file)[1]
        self.srcFdr = os.path.dirname(src_file)
        self.newFile = new_file
        # self.newDelimiter = new_delimiter
        # self.new_padding = new_padding
        self.operation = operation
        self.srcDelimiter, self.srcPadding, self.start, self.last = self.get_src_info()
        self.src_file_list = []

    def get_src_info(self):
        self.srcDelimiter = None
        self.srcPadding = None
        self.start = None
        self.last = None

        if re.search("\W%\d+d", self.srcFile):
            find_padding = re.search("\W%\d+d", self.srcFile).group()
            self.srcPadding = re.findall("%\d+d", find_padding)[0]
            self.srcDelimiter = find_padding.split(self.srcPadding)[0]
        elif "#" in os.path.splitext(self.srcFile)[0]:
            i = 0
            for letter in os.path.splitext(self.srcFile)[0]:
                if letter == "#":
                    i += 1
            self.srcPadding = "#" * i
        else:
            # search for delimiter in filename
            # hypothetically delimiter is one of ".", "_", "-"
            search_padding = re.search("[._-]\d+$", self.srcSequenceName)
            if search_padding:
                self.srcDelimiter = re.search("[._-]", search_padding.group()).group()

                frame_number_list = [os.path.splitext(f)[0].split(self.srcDelimiter)[1]
                                     for f in os.listdir(self.srcFdr)
                                     if f.split(self.srcDelimiter)[0] == self.srcSequenceName.split(self.srcDelimiter)[0]]

                frame_number_list.sort()
                for i in range(len(frame_number_list)):
                    if i > 0:
                        if int(frame_number_list[i - 1]) + 1 != int(frame_number_list[i]):
                            print "Sequence is missing frames."
                            break

                self.srcPadding = len(frame_number_list[-1]) * "#"
                self.srcDelimiter = search_padding.group().split(frame_number_list[0])[0]

            else:
                print "File is not a sequence file."

            # Find start and last frame of the sequence
            src_fdr_list = []
            for f in os.listdir(self.srcFdr):
                # find the correct sequence (there's potential there's more than one sequence in the folder)
                if f.split(self.srcDelimiter)[0] == os.path.basename(self.srcFile).split(self.srcDelimiter)[0]:
                    src_fdr_list.append(f)
            # Sort files in the source folder
            src_fdr_list.sort()
            self.start = os.path.splitext(src_fdr_list[0])[0].split(self.srcDelimiter)[1]
            self.last = os.path.splitext(src_fdr_list[-1])[0].split(self.srcDelimiter)[1]
            print "source delimiter: {}\n" \
                  "source padding: {}\n" \
                  "start frame: {}\n" \
                  "last frame: {}\n".format(self.srcDelimiter, self.srcPadding, self.start, self.last)
            return self.srcDelimiter, self.srcPadding, self.start, self.last

    def check_dest_file(self):


    def get_dest_info(self):
        "q:/xxx/xxx/xxxxx.xxx.ext"



    def make_dst_file(self):



    def rename_action(self):
        print""
        # make operation based on user decision, default is rename

        # make destination file




    # def list_src_dst(self):
    #     dst_file_list = []
    #
    #     for i in range(self.last):
    #         i += 1
    #         if i >= self.start:
    #             frame_number = self.src_padding % i
    #             src_file = "{0}/{1}{2}{3}{4}".format(
    #                 self.src_fdr,
    #                 self.src_file_name,
    #                 self.src_delimiter,
    #                 frame_number,
    #                 self.ext)
    #             src_file_list.append(src_file)
    #
    #             new_frame_number = new_padding % i
    #             dst_file = "{0}/{1}{2}{3}{4}".format(
    #                 self.newFdr,
    #                 new_filename,
    #                 new_delimiter,
    #                 new_frame_number,
    #                 self.ext)
    #             dst_file_list.append(dst_file)

#
# def rename_action(src_filename, new_filename, new_delimiter, new_padding):
#
#
#     # if re.search(".%\d+d", src_file_name):
#     #     src_padding = re.search(".%\d+d", src_file_name).group()
#     #     self.src_padding = re.findall("%\d+d", src_padding)[0]
#     #     self.src_delimiter = src_padding.split(self.src_padding)[0]
#     # elif "#" in os.path.splitext(src_file_name)[0]:
#     #     i = 0
#     #     for letter in os.path.splitext(src_file_name)[0]:
#     #         if letter == "#":
#     #             i += 1
#     #     self.src_padding = "#" * i
#     #
#     # if not re.search("%\d+d", new_padding):
#     #     # print re.search("%\d+d", new_padding)
#     #     if "#" in new_padding:
#     #         new_padding = "%0{}d".format(len(new_padding))
#     #     else:
#     #         self.notify_dialog('Warning', 'Please use either %xxd or # in padding', 'OK')
#     #         self.close_ui()
#     #         return
#
#
#     # List src and dst files
#     src_file_list = []
#     dst_file_list = []
#
#     for i in range(self.last):
#         i += 1
#         if i >= self.start:
#             frame_number = self.src_padding % i
#             src_file = "{0}/{1}{2}{3}{4}".format(
#                 self.src_fdr,
#                 self.src_file_name,
#                 self.src_delimiter,
#                 frame_number,
#                 self.ext)
#             src_file_list.append(src_file)
#
#             new_frame_number = new_padding % i
#             dst_file = "{0}/{1}{2}{3}{4}".format(
#                 self.newFdr,
#                 new_filename,
#                 new_delimiter,
#                 new_frame_number,
#                 self.ext)
#             dst_file_list.append(dst_file)
#
#     # Check if src file exists
#     not_exist_list = []
#     for file in src_file_list:
#         if not os.path.isfile(file):
#             not_exist_list.append(file)
#     if not_exist_list:
#         warning_msg = "Make sure the file exists: {}".format(self.source_file)
#         self.notify_dialog('Warning', warning_msg, 'OK')
#         return
#
#     # Check if dst file exists
#     exist_list = []
#     for file in dst_file_list:
#         if os.path.isfile(file):
#             # print file
#             exist_list.append(file)
#     print exist_list
#     over_write = True
#     if exist_list:
#         if len(exist_list) == len(src_file_list):
#             warning_msg = "{0}/{1} [{2} - {3}] already exits, do you want to over write those files?".format(
#                 self.newFdr, new_filename,
#                 os.path.splitext(os.path.basename(exist_list[0]))[0].split(new_delimiter)[1],
#                 os.path.splitext(os.path.basename(exist_list[-1]))[0].split(new_delimiter)[1]
#             )
#         else:
#             warning_msg = "Frames:\n{}\n already exist,\ndo you want to over write those files?".format(
#                 "\n".join(exist_list))
#
#         over_write = self.notify_dialog('Warning', warning_msg, 'OK')
#
#     if not over_write:
#         return
#
#     # Rename
#     if self.ui_main.RDO_SameDir.isChecked():
#         if over_write:
#             for count, file in enumerate(src_file_list):
#                 os.rename(file, dst_file_list[count])
#                 progress = int(round((float(count) + 2) / len(src_file_list) * 100.0))
#                 self.progressBar.setValue(progress)
#                 print progress
#                 print dst_file_list[count]
#                 print count
#     # Copy
#     else:
#         for count, file in enumerate(src_file_list):
#             if over_write and os.path.exists(dst_file_list[count]):
#                 os.remove(dst_file_list[count])
#
#             shutil.copy(file, dst_file_list[count])
#             if self.ui_main.RDO_Copy.isChecked:
#                 progress = int(round((float(count) + 2) / len(src_file_list) * 100.0))
#                 self.progressBar.setValue(progress)
#
#             # If move, delete old one
#             if self.ui_main.RDO_Move.isChecked():
#                 os.remove(file)
#                 progress = int(round((float(count) + 2) / len(src_file_list) * 100.0))
#                 self.progressBar.setValue(progress)
#
#                 pass


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option('-f', '--file', dest='source_file',
                      help='The source sequence path', metavar="FILE")
    parser.add_option('-n', '--new_sequence', dest='new_file', default=None,
                      help='new sequence name(just the name)')
    # parser.add_option('-d', '--new_delimiter', dest='new_delimiter', default=None,
    #                   help='new delimiter')
    # parser.add_option('-p', '--new_padding', dest='new_padding', default=None,
    #                   help='new padding')
    parser.add_option('-o', '--operation', dest='operation', default='rename',
                      help='Rename, Copy or Move, default is Rename')

    (options, ars) = parser.parse_args()
    for option in vars(options):
        # print option, getattr(options, option)
        # if not getattr(options, option):
        if not options.source_file:
            print"Please provide a sequence file."
            exit()

        # if not options.new_file:
        #     print "Please provide destination file path."
        #     exit()

    job = renameSequence(options.source_file, options.new_file, options.operation)
