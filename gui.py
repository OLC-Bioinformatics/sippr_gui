#!/usr/bin/python3
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QFileDialog, QLabel, QVBoxLayout, QMainWindow, QErrorMessage, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot, QTimer, Qt
from PyQt5 import QtGui
from argparse import ArgumentParser
import subprocess
from glob import glob
try:
    import xml.etree.cElementTree as ElementTree
except ImportError:
    import xml.etree.ElementTree as ElementTree
import sys
import os

testpath = os.path.abspath(os.path.dirname(__file__))
sys.path.append(testpath)
sys.path.append(os.path.join(testpath, 'demos'))
import design
import gar


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
        """

        """
        self.miseq_folder_btn.clicked.connect(self.folder_choose)

    def folder_choose(self):
        """

        """
        fname = QFileDialog.getExistingDirectory(self,
                                                 'Select MiSeq Folder',
                                                 '/home/adamkoziol/Bioinformatics/miseq_data')
        self.miseqfolder = os.path.split(fname)[-1]
        if self.miseqfolder:
            self.run_name.setText('MiSeq Run Name: {}'.format(self.miseqfolder))
            self.readlength_determination()
            try:
                if self.cycles >= int(self.readlengthforward) + 16:
                    self.analysis_btn.setEnabled(True)
                else:
                    pass
            except ValueError:
                pass

    @staticmethod
    def message(window_title, short, detailed=None, disable=True):
        """
        Populate details to display in message box
        :param window_title: The name of the window
        :param short: Short description of the message
        :param detailed: Detailed description of the message
        :param disable: Boolean to disable window buttons
        """
        # Create the message box
        error = QMessageBox()
        error.setWindowTitle(window_title)
        error.setText(short)
        if detailed:
            error.setDetailedText(detailed)
        if disable:
            # Disable the minimise, maximise, and close buttons for the window
            error.setWindowFlags(Qt.CustomizeWindowHint)
        error.exec()

    def readlength_determination(self):
        """

        """
        # Count the number of completed cycles in the run of interest
        try:
            #
            cycle_folders = \
                glob(os.path.join(self.miseqpath, self.miseqfolder, 'Data', 'Intensities', 'BaseCalls', 'L001', 'C*'))
            self.cycles = len(cycle_folders)
            _ = cycle_folders[0]
            self.parseruninfo()
            self.forwardreads.setText('Forward Read Length: {}'.format(self.readlengthforward))
            self.reversereads.setText('Reverse Read Length: {}'.format(self.readlengthreverse))
        except IndexError:
            self.message('IndexError', 'Not a valid MiSeq run folder',
                         detailed='Could not find the necessary directories in the supplied folder: {}'
                         .format(os.path.join(self.miseqpath, self.miseqfolder)))
            print('Something went wrong')

    def parseruninfo(self):
        """
        Extract the number of forward and reverse reads in the run from the RunInfo.xml file
        """
        #
        try:
            runinfo = ElementTree.ElementTree(file=os.path.join(self.miseqpath, self.miseqfolder, 'RunInfo.xml'))
            #
            for elem in runinfo.iter():
                for run in elem:
                    try:
                        num_cycles = run.attrib['NumCycles']
                        if run.attrib['Number'] == '1':
                            self.readlengthforward = num_cycles
                        if run.attrib['Number'] == '4':
                            self.readlengthreverse = num_cycles
                    except KeyError:
                        pass
        except IOError:
            pass

    def start_analyses(self):
        """

        """
        self.analysis_btn.clicked.connect(self.run)
        self.analysis_btn.setEnabled(False)

    def run(self):
        """

        """
        if self.miseqfolder:
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
        """

        """
        command = 'docker run -i --rm -v /mnt/nas:/mnt/nas ' \
                  '-v /home/adamkoziol/Bioinformatics:/home/ubuntu/Bioinformatics ' \
                  'olcbioinformatics/sipprverse:latest /bin/bash -c "source activate genesippr && python method.py ' \
                  '-m /home/ubuntu/Bioinformatics/ -f 161104_M02466_0002_000000000-AV4G5 -r1 70 -r2 0 -c ' \
                  '/home/ubuntu/Bioinformatics/sippr/gui/SampleSheet.csv ' \
                  '-r /mnt/nas/assemblydatabases/0.2.3/databases ' \
                  '-d /home/ubuntu/Bioinformatics/sippr/gui/161104_M02466_0002_000000000-AV4G5/sequences ' \
                  '-o /home/ubuntu/Bioinformatics/sippr/gui/161104_M02466_0002_000000000-AV4G5"'
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        #
        print(self.samplesheet)
        gar.GAR(self)
        self.sippr_clear()

    def log(self):
        """
        Set up the timer to update the output text box with the portal.log once every second
        """

        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.log_read)
        self.timer.start()
        self.output.setEnabled(True)

    def log_read(self):
        """
        Read the pipeline stdout from the portal.log
        """
        try:
            log = open('/home/adamkoziol/Bioinformatics/sippr/gui/161104_M02466_0002_000000000-AV4G5/portal.log').readlines()
            for entry in log:
                if 'SampleSheet:' in entry:
                    self.samplesheet = entry.split()[-1]
        except FileNotFoundError:
            log = str()
            self.samplesheet = str()
        try:
            self.output.setText(''.join(log))
        except RuntimeError:
            pass

    def sippr_clear(self):
        """
        Stop the timer, and enable buttons as necessary
        """
        self.timer.stop()
        self.miseq_folder_btn.setEnabled(True)
        self.reports.setEnabled(True)
        try:
            os.remove('/home/adamkoziol/Bioinformatics/sippr/gui/portal.log')
        except:
            pass

    def __init__(self, args):
        super(self.__class__, self).__init__()
        self.miseqpath = os.path.join(args.miseqpath)
        self.referencefilepath = '/home/ubuntu/targets'
        self.readlengthforward = 'full'
        self.readlengthreverse = 'full'
        self.copy = True
        self.miseqfolder = str()
        self.cycles = int()
        self.samplesheet = str()
        self.threadpool = QThreadPool()
        self.timer = QTimer()
        # self.error = ''
        self.setupUi(self)
        self.main()


if __name__ == '__main__':
    # Parser for arguments
    parser = ArgumentParser(description='GUI for genesippr')
    parser.add_argument('-o', '--outputpath',
                        required=True,
                        help='Path to directory in which report folder is to be created')
    parser.add_argument('-m', '--miseqpath',
                        required=True,
                        help='Path of the folder containing MiSeq run data folder')
    parser.add_argument('-c', '--customsamplesheet',
                        help='Path of folder containing a custom sample sheet (still must be named "SampleSheet.csv")')
    # Get the arguments into an object
    arguments = parser.parse_args()
    app = QApplication(sys.argv)
    ex = GUI(arguments)
    ex.show()
    sys.exit(app.exec_())
