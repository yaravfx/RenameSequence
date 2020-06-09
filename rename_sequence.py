import nuke
import os
import re
import shutil
import threading

if nuke.NUKE_VERSION_MAJOR < 11:
    from PySide import QtCore
    from PySide import QtUiTools
    from PySide.QtGui import *

else:
    from PySide2 import QtCore, QtUiTools, QtGui
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
    # from PySide2 import QtWidgets
    # from PySide2 import QtCore as QtCore
    # from PySide2 import QtUiTools

# Global Variables
tb_path = os.path.dirname(os.path.realpath(__file__))
ui_path = os.path.join(tb_path, 'UI', 'RenameSequence.ui')


class RenameSequenceUI(QMainWindow):
    def __init__(self, parent=QApplication.activeWindow()):
        super(RenameSequenceUI, self).__init__(parent)

        self.source_file = nuke.selectedNodes()[0]['file'].value()
        self.ext = os.path.splitext(self.source_file)[1]
        self.src_fdr = os.path.dirname(self.source_file)
        self.newFdr = self.src_fdr
        self.start = int(nuke.selectedNode()['first'].value())
        self.last = int(nuke.selectedNode()['last'].value())
        self.progressText = "TEST"
        # Load the UI
        ui_loader = QtUiTools.QUiLoader()

        # Load the main UI
        ui_file = QtCore.QFile(ui_path)
        ui_file.open(QtCore.QFile.ReadOnly)
        self.ui_main = ui_loader.load(ui_file)

        # Setup the UI
        # self.setWindowFlags(QtCore.Qt.Tool)
        self.setCentralWidget(self.ui_main)
        self.setWindowTitle("Rename Sequence")
        self.setGeometry(560, 400, 650, 0)
        self.setup_ui()

        self.define_connections()
        self.panel_control()

        # self.progressBar = QProgressBar(self)
        #
        # self.progressBar.setGeometry(250, 313, 300, 25)
        # print self.ui_main.y()
        # # self.btnStart = QPushButton('Start', self)

    def close_ui(self):
        self.close()

    def setup_ui(self):
        self.progressBar = self.ui_main.PGB_ProgressBar
        self.progressBar.setValue(0)

        self.source_file = nuke.selectedNodes()[0]['file'].value()

        self.ui_main.TXT_SourceFile.setText(self.source_file)
        self.ui_main.TXT_SourceFile.setEnabled(False)

        src_file_name = os.path.basename(self.source_file)
        src_file_name = os.path.splitext(src_file_name)[0]
        # print src_file_name
        # print re.search(".%\d+d", src_file_name)
        if re.search(".%\d+d", src_file_name):
            src_padding = re.search(".%\d+d", src_file_name).group()
            self.src_padding = re.findall("%\d+d", src_padding)[0]
            self.src_delimiter = src_padding.split(self.src_padding)[0]
        elif "#" in os.path.splitext(src_file_name)[0]:
            i = 0
            for letter in os.path.splitext(src_file_name)[0]:
                if letter == "#":
                    i += 1
            self.src_padding = "#" * i

        else:
            src_padding = "None"
            self.src_padding = "None"
            self.src_delimiter = "None"

        # print src_file_name.split(self.src_padding)
        self.src_file_name = src_file_name.split(self.src_delimiter + self.src_padding)[0]
        self.ui_main.TXT_SrcFileName.setText(self.src_file_name)
        self.ui_main.TXT_SrcDelimiter.setText(self.src_delimiter)
        self.ui_main.TXT_SrcPadding.setText(self.src_padding)
        self.ui_main.TXT_SrcFileName.setEnabled(False)
        self.ui_main.TXT_SrcDelimiter.setEnabled(False)
        self.ui_main.TXT_SrcPadding.setEnabled(False)
        self.ui_main.RDO_SameDir.setChecked(True)
        self.ui_main.TXT_PickFdr.setEnabled(False)
        self.ui_main.BTN_PickFdr.setEnabled(False)

        self.ui_main.TXT_NewFileName.setText(self.src_file_name)
        self.ui_main.TXT_NewDelimiter.setText(self.src_delimiter)
        self.ui_main.TXT_NewPadding.setText(self.src_padding)

    def define_connections(self):
        self.ui_main.RDO_SameDir.clicked.connect(self.panel_control)
        self.ui_main.RDO_Move.clicked.connect(self.panel_control)
        self.ui_main.RDO_Copy.clicked.connect(self.panel_control)
        self.ui_main.BTN_PickFdr.clicked.connect(self.pick_fdr)
        self.ui_main.BTN_Preview.clicked.connect(self.preview)
        self.ui_main.BTN_Run.clicked.connect(self.run_action)

    def panel_control(self):
        if self.ui_main.RDO_SameDir.isChecked():
            self.newFdr = self.src_fdr
            self.ui_main.TXT_PickFdr.setEnabled(False)
            self.ui_main.BTN_PickFdr.setEnabled(False)

        if self.ui_main.RDO_Move.isChecked() or self.ui_main.RDO_Copy.isChecked():
            self.ui_main.TXT_PickFdr.setEnabled(True)
            self.ui_main.BTN_PickFdr.setEnabled(True)

    def pick_fdr(self):
        # openDir = os.path.dirname(self.source_file)
        # outPath = QtWidgets.QFileDialog.getOpenFileName(self, "Pick a directory", openDir)
        outPath = QFileDialog.getExistingDirectory(self, "Pick a directory", self.src_fdr, QFileDialog.ShowDirsOnly)
        print outPath
        if outPath:
            self.newFdr = outPath
            self.ui_main.TXT_PickFdr.setText(str(outPath))

    def preview(self):
        self.newFileName = self.ui_main.TXT_NewFileName.text()
        self.newDelimiter = self.ui_main.TXT_NewDelimiter.text()
        self.newPadding = self.ui_main.TXT_NewPadding.text()

        if self.newFileName and self.newDelimiter and self.newPadding:
            print "running preview"
            new_filename = "{0}{1}{2}{3}".format(
                                           self.newFileName,
                                           self.newDelimiter,
                                           self.newPadding,
                                           self.ext)

            new_file = os.path.join(self.newFdr, new_filename)
            new_file = new_file.replace("\\", "/")
            print new_file

            self.ui_main.LBL_NewFile.setText(new_file)
        else:
            print "pls put in info"

    def rename_action(self):
        self.newFileName = self.ui_main.TXT_NewFileName.text()
        self.newDelimiter = self.ui_main.TXT_NewDelimiter.text()
        self.newPadding = self.ui_main.TXT_NewPadding.text()
        print self.newPadding

        if not re.search("%\d+d", self.newPadding):
            # print re.search("%\d+d", self.newPadding)
            if "#" in self.newPadding:
                self.newPadding = "%0{}d".format(len(self.newPadding))
            else:
                self.notify_dialog('Warning', 'Please use either %xxd or # in padding', 'OK')
                self.close_ui()
                return

        # List src and dst files
        src_file_list = []
        dst_file_list = []

        for i in range(self.last):
            i += 1
            if i >= self.start:
                frame_number = self.src_padding % i
                src_file = "{0}/{1}{2}{3}{4}".format(
                    self.src_fdr,
                    self.src_file_name,
                    self.src_delimiter,
                    frame_number,
                    self.ext)
                src_file_list.append(src_file)

                new_frame_number = self.newPadding % i
                dst_file = "{0}/{1}{2}{3}{4}".format(
                    self.newFdr,
                    self.newFileName,
                    self.newDelimiter,
                    new_frame_number,
                    self.ext)
                dst_file_list.append(dst_file)

        # Check if src file exists
        not_exist_list = []
        for file in src_file_list:
            if not os.path.isfile(file):
                not_exist_list.append(file)
        if not_exist_list:
            warning_msg = "Make sure the file exists: {}".format(self.source_file)
            self.notify_dialog('Warning', warning_msg, 'OK')
            return

        # Check if dst file exists
        exist_list = []
        for file in dst_file_list:
            if os.path.isfile(file):
                # print file
                exist_list.append(file)
        print exist_list
        over_write = True
        if exist_list:
            if len(exist_list) == len(src_file_list):
                warning_msg = "{0}/{1} [{2} - {3}] already exits, do you want to over write those files?".format(
                    self.newFdr, self.newFileName,
                    os.path.splitext(os.path.basename(exist_list[0]))[0].split(self.newDelimiter)[1],
                    os.path.splitext(os.path.basename(exist_list[-1]))[0].split(self.newDelimiter)[1]
                )
            else:
                warning_msg = "Frames:\n{}\n already exist,\ndo you want to over write those files?".format(
                        "\n".join(exist_list))

            over_write = self.notify_dialog('Warning', warning_msg, 'OK')

        if not over_write:
            return

        # Rename
        if self.ui_main.RDO_SameDir.isChecked():
            if over_write:
                for count, file in enumerate(src_file_list):
                    os.rename(file, dst_file_list[count])
                    progress = int(round((float(count) + 2) / len(src_file_list) * 100.0))
                    self.progressBar.setValue(progress)
                    print progress
                    print dst_file_list[count]
                    print count
        # Copy
        else:
            for count, file in enumerate(src_file_list):
                if over_write and os.path.exists(dst_file_list[count]):
                    os.remove(dst_file_list[count])

                shutil.copy(file, dst_file_list[count])
                if self.ui_main.RDO_Copy.isChecked:
                    progress = int(round((float(count) + 2) / len(src_file_list) * 100.0))
                    self.progressBar.setValue(progress)

                # If move, delete old one
                if self.ui_main.RDO_Move.isChecked():
                    os.remove(file)
                    progress = int(round((float(count) + 2) / len(src_file_list) * 100.0))
                    self.progressBar.setValue(progress)

                    pass

        # self.showProgressbar()

    def run_action(self):
        thread = threading.Thread(None, self.rename_action())
        thread.start()

    def notify_dialog(self, title, message, action_yes):
        msg_dialog = QMessageBox()
        msg_dialog.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        msg_dialog.setModal(True)
        msg_dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        msg_dialog.setWindowTitle(title)
        msg_dialog.setText(message)

        BTN_Yes = QPushButton(action_yes)
        msg_dialog.addButton(BTN_Yes, QMessageBox.YesRole)

        BTN_No = QPushButton("Cancel")
        msg_dialog.addButton(BTN_No, QMessageBox.NoRole)

        answer = msg_dialog.exec_()
        if answer is 0:
            return True
        else:
            return False

    def show_ui(self):
        self.show()
        self.activateWindow()

    def open(self):
        self.show_ui()
