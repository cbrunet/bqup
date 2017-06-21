import sys
from PyQt5.QtWidgets import QApplication

from mainwindow import MainWindow
from widgets.branches.branchesmodel import BranchesModel


class BqupApplication(QApplication):

    def __init__(self):
        super().__init__(sys.argv)

        self.setApplicationName("bqup")
        self.setOrganizationDomain("cbrunet.net")
        self.setOrganizationName("cbrunet")

        self.branches = BranchesModel()


if __name__ == '__main__':

    app = BqupApplication()
    w = MainWindow()
    w.show()

    sys.exit(app.exec_())
