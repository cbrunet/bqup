from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFileDialog


class LocationDialog(QFileDialog):

    def __init__(self, parent=None):
        caption = QApplication.translate(self.__class__.__name__,
                                         "Select Backup Location")
        super().__init__(parent, caption)
        self.setAcceptMode(QFileDialog.AcceptSave)
        self.setFileMode(QFileDialog.DirectoryOnly)
        self.setOption(QFileDialog.ShowDirsOnly)

    def accept(self):
        location = self.selectedFiles()[0]
        branches_model = QApplication.instance().branches
        branches_model.addLocation(location)
        super().accept()
