#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QFileDialog, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot, QTimer
from PyQt5 import QtGui
import subprocess
import sys
import os

testpath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(testpath, 'demos'))
import design


class Worker(QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    """
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        """
        Initialise the runner function with passed args, kwargs.
        """

        # Retrieve args/kwargs here; and fire processing using them
        self.fn(*self.args, **self.kwargs)


class GUI(QMainWindow, design.Ui_GeneSippr):

    def main(self):
        self.folder_browse()
        self.start_analyses()

    def folder_browse(self):
        self.miseq_folder_btn.clicked.connect(self.folder_choose)

    def folder_choose(self):
        fname = QFileDialog.getExistingDirectory(self,
                                                 'Select MiSeq Folder',
                                                 '/mnt/nas/Forest/live_sipping_testing/miseq_data')
        self.miseq_dir = os.path.split(fname)[-1]
        if self.miseq_dir:
            self.analysis_btn.setEnabled(True)

    def start_analyses(self):
        self.analysis_btn.clicked.connect(self.run)
        self.analysis_btn.setEnabled(False)

    def run(self):
        if self.miseq_dir:
            print('Ready to go!')
            worker = Worker(self.sippr)
            self.miseq_folder_btn.setEnabled(False)
            self.analysis_btn.setEnabled(False)
            self.output.setEnabled(True)
            self.log()
            self.threadpool.start(worker)
        else:
            print('Hold up!')

    def sippr(self):
        command = 'docker run -i --rm -v /mnt/nas:/mnt/nas ' \
                  '-v /home/adamkoziol/Bioinformatics:/home/ubuntu/Bioinformatics ' \
                  'olcbioinformatics/sipprverse:latest /bin/bash -c "source activate genesippr && python method.py ' \
                  '-m /home/ubuntu/Bioinformatics/ -f 161104_M02466_0002_000000000-AV4G5 -r1 70 -r2 0 -c ' \
                  '/home/ubuntu/Bioinformatics/sippr/method/SampleSheet.csv ' \
                  '-r /mnt/nas/assemblydatabases/0.2.3/databases ' \
                  '-d /home/ubuntu/Bioinformatics/sippr/method/sequences ' \
                  '-o /home/ubuntu/Bioinformatics/sippr/method"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        self.output.setEnabled(False)
        # self.output.deleteLater()
        self.miseq_folder_btn.setEnabled(True)
        self.reports.setEnabled(True)

    def log(self):
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.log_read)
        self.timer.start()
        self.output.setEnabled(True)

    def log_read(self):
        try:
            log = open('/home/adamkoziol/Bioinformatics/sippr/method/portal.log').readlines()
        except FileNotFoundError:
            log = str()
        try:
            self.output.setText(''.join(log))
        except RuntimeError:
            pass

    def __init__(self):
        super(self.__class__, self).__init__()
        self.miseq_dir = str()
        self.threadpool = QThreadPool()
        self.timer = QTimer()
        self.setupUi(self)
        self.main()


class Example(QMainWindow):

    def main(self):

        QToolTip.setFont(QFont('SansSerif', 10))

        self.setToolTip('This is a <b>QWidget</b> widget')

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('GeneSippr')
        self.folder_browse()
        self.start_analyses()

        self.show()

    def log(self):

        self.log_widget.setLayout(self.layout)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.log_read)
        self.timer.start()
        self.layout.addWidget(self.output)
        self.setCentralWidget(self.log_widget)

    def folder_browse(self):
        self.folder_btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.folder_btn.resize(self.folder_btn.sizeHint())
        # btn.move(50, 50)
        self.folder_btn.clicked.connect(self.folder_choose)

    def folder_choose(self):
        fname = QFileDialog.getExistingDirectory(self,
                                                 'Select MiSeq Folder',
                                                 '/mnt/nas/Forest/live_sipping_testing/miseq_data')
        self.miseq_dir = os.path.split(fname)[-1]
        if self.miseq_dir:
            self.analysis_btn.setEnabled(True)

    def start_analyses(self):

        self.analysis_btn.setToolTip('This is a <b>QPushButton</b> widget')
        self.analysis_btn.resize(self.analysis_btn.sizeHint())
        self.analysis_btn.move(150, 150)
        self.analysis_btn.clicked.connect(self.run)
        self.analysis_btn.setEnabled(False)

    def run(self):
        if self.miseq_dir:
            print('Ready to go!')
            worker = Worker(self.sippr)
            self.folder_btn.setEnabled(False)
            self.analysis_btn.setEnabled(False)
            self.log()
            self.threadpool.start(worker)
        else:
            print('Hold up!')

    def sippr(self):
        command = 'docker run -i --rm -v /mnt/nas:/mnt/nas ' \
                  '-v /home/adamkoziol/Bioinformatics:/home/ubuntu/Bioinformatics ' \
                  'olcbioinformatics/sipprverse:latest /bin/bash -c "source activate genesippr && python method.py ' \
                  '-m /home/ubuntu/Bioinformatics/ -f 161104_M02466_0002_000000000-AV4G5 -r1 70 -r2 0 -c ' \
                  '/home/ubuntu/Bioinformatics/sippr/method/SampleSheet.csv ' \
                  '-r /mnt/nas/assemblydatabases/0.2.3/databases ' \
                  '-d /home/ubuntu/Bioinformatics/sippr/method/sequences ' \
                  '-o /home/ubuntu/Bioinformatics/sippr/method"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(self.miseq_dir)
        self.layout.removeWidget(self.log_widget)
        self.log_widget.deleteLater()
        self.log_widget = None
        self.folder_btn.setEnabled(True)

    def log_read(self):
        try:
            log = open('/home/adamkoziol/Bioinformatics/sippr/method/portal.log').readlines()
        except FileNotFoundError:
            log = str()
        try:
            self.output.setText("Log: %s" % ''.join(log))
        except RuntimeError:
            pass

    def __init__(self):
        super().__init__()
        self.miseq_dir = str()
        self.layout = QVBoxLayout()
        self.folder_btn = QPushButton('Select MiSeq Folder', self)
        self.analysis_btn = QPushButton('Run Analyses', self)
        self.threadpool = QThreadPool()
        self.timer = QTimer()
        self.output = QLabel('Log')
        self.log_widget = QWidget()
        self.main()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = GUI()
    ex.show()
    sys.exit(app.exec_())
