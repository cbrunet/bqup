from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QSplitter

from widgets.branches.branchesview import BranchesView
from widgets.backupbrowser.browserview import BackupBrowserView


class BrowseTab(QSplitter):

    def __init__(self):
        super().__init__()

        self.branches = BranchesView()
        self.branches.setModel(QApplication.instance().branches)

        self.backups = BackupBrowserView()

        self.addWidget(self.branches)
        self.addWidget(self.backups)
