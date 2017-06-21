from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QTabWidget

from layouts.browse import BrowseTab
from layouts.filesystem import FileSystemTab
from layouts.config import ConfigTab
from layouts.schedule import ScheduleTab

from widgets.branches.locationdialog import LocationDialog

import version


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.browse_tab = BrowseTab()
        self.filesystem_tab = FileSystemTab()
        self.config_tab = ConfigTab()
        self.schedule_tab = ScheduleTab()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.browse_tab, self.tr("Browse"))
        self.tabs.addTab(self.filesystem_tab, self.tr("Filesystem"))
        self.tabs.addTab(self.config_tab, self.tr("Config"))
        self.tabs.addTab(self.schedule_tab, self.tr("Schedule"))

        self.setCentralWidget(self.tabs)

        self.init_menubar()

    def init_menubar(self):
        self.file_menu = self.menuBar().addMenu(self.tr("File"))

        self.actions_new_location = self.file_menu.addAction(
            self.tr("New Backup Location..."), self.on_action_new_location)
        self.file_menu.addSeparator()
        self.actions_quit = self.file_menu.addAction(
            self.tr("Quit"), self.on_action_quit, QKeySequence.Quit)

        self.help_menu = self.menuBar().addMenu(self.tr("Help"))

        self.actions_about = self.help_menu.addAction(
            self.tr("About bqup..."), self.on_action_about)

    def on_action_new_location(self):
        dialog = LocationDialog(self)
        dialog.exec_()

    def on_action_quit(self):
        QApplication.instance().quit()

    def on_action_about(self):
        QMessageBox.about(self, self.tr("About bqup"),
                          self.tr(version.about))
