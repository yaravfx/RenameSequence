# coding:utf8

import argparse
import os
import re


class FindSequence:
    def __init__(self, fdrPath):
        self.fdrPath = fdrPath
        self.sequenceDict = {}

    def lss(self):
        """
        print the list of sequences
        :return:
        """
        self.get_sequences()

        for key, value in self.sequenceDict.items():
            value.sort()
            if len(value) > 1:
                # if there's missing frames
                missing_frames = self.find_missing_frame(value)
                if missing_frames:
                    print "{}  {}    {}-{}-{}".format(len(value), key, value[0][0], "-".join(missing_frames), value[-1][0])
                else:
                    print "{}  {}    {}-{}".format(len(value), key, value[0][0], value[-1][0])
            else:  # single frame files
                print "{}  {}".format(len(value), key)

    def find_missing_frame(self, frame_numbers):
        missing_frames = []
        count = 0
        for index, frames in enumerate(frame_numbers):
            if index < len(frame_numbers) - 1:
                # print index
                frame = frames[0]
                # print frame
                if frame_numbers[index+1][0] - frame != 1:
                    lst = []
                    # print "missing frame"
                    count += 1
                    # print frame, frame_numbers[index+1][0]
                    lst.append(str(frame))
                    lst.append(str(frame_numbers[index+1][0]))
                    missing_string = "{} {}".format(str(frame), str(frame_numbers[index+1][0]))
                    missing_frames.append(missing_string)
        return missing_frames

    def get_sequences(self):
        """
        generates two lists of potenial names based on the numbers in the filename.
        compare between the one file and the next file until the second last file in the folder.
        the correct sequence name should be the same as the potential name of the next frame file.

        :return: a dictionary of sequence name and the value of a lists of frame numbers list,
        for single frame files the value is a list of itself.
        """
        files = []
        for f in os.listdir(self.fdrPath):
            if os.path.isfile(os.path.join(self.fdrPath, f)):
                files.append(f)
        files.sort()
        for index, filename in enumerate(files):
            found_name = False  # use this to found the last frame file
            if index < len(files) - 1:
                frame_numbers = self.find_numbers(filename)
                next_frame_numbers = self.find_numbers(files[index+1])
                if not frame_numbers:  # if there's no number, it's a new sequence
                    self.sequenceDict[filename] = [filename]
                    continue

                potential_name = []
                for n in frame_numbers:
                    potential_name.append(self.get_sequence_info(filename, n))
                first_frame_numbers = {}  # the first frame will be missed, so i'll add it later
                for n in frame_numbers:
                    first_frame_numbers[self.get_sequence_info(filename, n)] = n

                frame_coverage = []
                for n in next_frame_numbers:
                    # for name in potential_name:
                    next_frame_name = self.get_sequence_info(files[index+1], n)
                    if next_frame_name in potential_name:
                        sequence_name = next_frame_name
                        found_name = True
                        if sequence_name not in self.sequenceDict.keys():
                            self.sequenceDict[sequence_name] = frame_coverage
                        self.sequenceDict[sequence_name].append(n)

                        for sequence, frames in first_frame_numbers.items():
                            if sequence == sequence_name:
                                if frames not in self.sequenceDict[sequence]:
                                    self.sequenceDict[sequence].append(frames)

                for name in potential_name:  # this will include the last frame of the sequence
                    if name in self.sequenceDict.keys():
                        found_name = True

                if not found_name:
                    # include the left over files,
                    # which should be the single frame file with a number in the name
                    self.sequenceDict[filename] = [filename]

    def get_sequence_info(self, filename, frame_numbers):
        """
        prints the sequence info in a format based on the numbers that are found in the name
        :param filename: denoise_v001_test_01.047.exr
        :param frame_numbers: [47, 3, 21, 24]/[1, 3, 9, 12]
        :return:denoise_v001_test_01.%03d.exr/denoise_v%03d_test_01.047.exr
        """
        start_i = frame_numbers[2]
        last_i = frame_numbers[3]
        return "{}%0{}d{}".format(filename[:start_i], frame_numbers[1], filename[last_i:])

    def find_numbers(self, frame_name):
        """
        get a list of all the numbers in the file name. this will be used to create potential names of the sequence
        [number, length, start index, end index]
        :param frame_name: "denoise_v001_test_01.047.exr"
        :return: [[1, 3, 9, 12], [1, 2, 18, 20], [47, 3, 21, 24]]
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
# fdr_path = "D:/Python_Project/test_lss/"

# job = FindSequence(fdr_path)
# job.lss()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Finding sequences of files")
    parser.add_argument('folder', metavar='F', type=str, help='Folder path')

    args = parser.parse_args()
    job = FindSequence(args.folder)
    job.lss()
