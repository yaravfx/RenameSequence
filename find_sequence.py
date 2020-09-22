# coding:utf8

import argparse
import os
import difflib
import re
import numbers
import time


class findSequence:
    def __init__(self, fdrPath):
        self.fdrPath = fdrPath
        self.sequenceDict = {}

    def lss(self):
        """
        print the list of sequences
        :return:
        """
        self.compare_files()
        # print self.sequenceDict

        for key, value in self.sequenceDict.items():
            value.sort()
            if len(value) > 1:
                print "{} {}    {}-{}".format(len(value), key, value[0][0], value[-1][0])
            else:
                print "{} {}".format(len(value), key)

    def compare_files(self):
        """
        compare between the one file and the next file until the second last file in the folder.
        :return:
        """
        files = []
        for f in os.listdir(self.fdrPath):
            if os.path.isfile(os.path.join(self.fdrPath, f)):
                files.append(f)
        files.sort()

        for index, filename in enumerate(files):
            print filename
            if index < len(files) - 1:
                frame_numbers = self.find_numbers(filename)
                next_frame_numbers = self.find_numbers(files[index+1])
                if not frame_numbers:  # if there's no number, it's a new sequence
                    self.sequenceDict[filename] = [filename]
                    continue

                print "here"
                potential_name = []
                for n in frame_numbers:
                    potential_name.append(self.get_sequence_info(filename, n))
                print "potential name: ", potential_name

                first_frame_numbers = {}  # the first frame will be missed, so i'll add it later
                for n in frame_numbers:
                    first_frame_numbers[self.get_sequence_info(filename, n)] = n

                frame_coverage = []
                for n in next_frame_numbers:
                    # for name in potential_name:
                    print self.get_sequence_info(files[index+1], n)
                    if self.get_sequence_info(files[index+1], n) in potential_name:
                        sequence_name = self.get_sequence_info(files[index+1], n)
                        if sequence_name not in self.sequenceDict.keys():
                            self.sequenceDict[sequence_name] = frame_coverage
                        self.sequenceDict[sequence_name].append(n)

                        for sequence, frames in first_frame_numbers.items():
                            if sequence == sequence_name:
                                if frames not in self.sequenceDict[sequence]:
                                    self.sequenceDict[sequence].append(frames)



    def get_sequence_info(self, filename, frame_numbers):
        start_i = frame_numbers[2]
        last_i = frame_numbers[3]
        return "{}%0{}d{}".format(filename[:start_i], frame_numbers[1], filename[last_i:])

    def find_numbers(self, frame_name):
        """
        get a list of all the numbers in the file name. returns a list consists of list of the number itself,
        the length of the number, the start index and end index of the number.
        :param frame_name: "denoise_test_1_v002.028.exr"
        :return: [[1, 1, 13, 14], [2, 3, 16, 19], [28, 3, 20, 23]]
        """
        numbers = []
        for digits in re.finditer("\d+", frame_name):
            current_number = []
            current_number.append(int(digits.group()))
            current_number.append(len(digits.group()))
            current_number.append(digits.start())
            current_number.append(digits.end())
            numbers.append(current_number)
        return numbers

# fdr_path = "D:\PERSONAL_PROJECT\LJTX_E01_S04C081\precomp\denoise_02"
# fdr_path = "D:\PERSONAL_PROJECT\LJTX_E01_S04C081\precomp\\test_01"
# fdr_path = "D:/PERSONAL_PROJECT/LJTX_E01_S04C081/precomp/test_05/"
fdr_path = "D:/Python_Project/test_lss/"

start = time.time()
job = findSequence(fdr_path)
job.lss()
print
print time.time() - start
#
# if job.find_numbers('alpha.txt'):
#     print True
# else:
#     print False
# print job.sequenceDict

# if __name__ == "__main__":
#
#     parser = argparse.ArgumentParser(description="Finding sequences of files")
#     parser.add_argument('folder', metavar='F', type=str, help='Folder path')
#
#     args = parser.parse_args()
#     job = findSequence(args.folder)
#     job.lss()
