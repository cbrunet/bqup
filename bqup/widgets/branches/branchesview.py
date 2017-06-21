from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMenu
from PyQt5.QtWidgets import QTreeView

import os
import platform
import subprocess


class BranchesView(QTreeView):

    def __init__(self):
        super().__init__()

    def contextMenuEvent(self, event):
        index = self.indexAt(event.pos())

        menu = QMenu()
        browse = menu.addAction(self.tr("Open in file manager"))
        if not index.isValid() or index.parent() != QModelIndex():
            browse.setEnabled(False)
        menu.addSeparator()
        menu.addAction(self.window().actions_new_location)

        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == browse:
            self.on_browse(index)

    def on_browse(self, index):
        location = index.data()

        if platform.system() == "Windows":
            os.startfile(location)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", location])
        else:
            subprocess.Popen(["xdg-open", location])
