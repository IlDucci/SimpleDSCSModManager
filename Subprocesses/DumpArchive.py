import os

from PyQt5 import QtCore 
from Utils.MBE import mbe_batch_unpack

class DumpArchiveWorkerThread(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    messageLog = QtCore.pyqtSignal(str)
    updateMessageLog = QtCore.pyqtSignal(str)
    lockGui = QtCore.pyqtSignal()
    releaseGui = QtCore.pyqtSignal()
    
    def __init__(self, archive, source_folder, dump_folder, dscstools_handler, extract_method, parent=None):
        super().__init__(parent)
        self.archive = archive
        self.source_folder = source_folder
        self.dump_folder = dump_folder
        self.dscstools_handler = dscstools_handler
        self.extract_method = extract_method
        
    def run(self):
        try:
            self.lockGui.emit()
            self.messageLog.emit(f"Extracting {self.dscstools_handler.base_archive_name(self.archive)} to {self.dump_folder}...")
            self.extract_method(self.archive, self.source_folder, self.dump_folder, self.messageLog, self.updateMessageLog)
            self.messageLog.emit("Extraction successful.")
        except Exception as e:
            self.messageLog.emit(f"The following error occured when trying to extract {self.dscstools_handler.base_archive_name(self.archive)}: {e}")
            raise e
        finally:
            self.releaseGui.emit()
            self.finished.emit()
