from PyQt5.QtCore import Qt
from PyQt5.QtCore import QAbstractItemModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtCore import QSettings

import os.path
import subprocess


class BranchesModel(QAbstractItemModel):

    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.locations = self.settings.value("locations", [])
        self.branches = {}

    def addLocation(self, location):
        result = subprocess.run(["bup", "-d", location, "init"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=True)

        self.locations.append(location)
        self.locations.sort()
        row = self.locations.index(location)

        self.beginInsertRows(QModelIndex(), row, row)
        self.settings.setValue("locations", self.locations)
        self.endInsertRows()

    def fetchBranches(self, location):
        result = subprocess.run(["bup", "-d", location, "ls"],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                check=True)
        branches = result.stdout.decode('utf-8').strip().split('\n')

        row = self.locations.index(location)
        index = self.index(row, 0)

        existing = self.branches.get(location, [])
        self.branches[location] = existing

        for branch in branches:
            if branch and branch not in existing:
                self.branches[location].append(branch)
                self.branches[location].sort()
                row = self.branches[location].index(branch)
                self.beginInsertRows(index, row, row)
                self.endInsertRows()

        for branch in existing:
            if branch not in branches:
                row = self.branches[location].index(branch)
                self.beginRemoveRows(index, row, row)
                del self.branches[location][row]
                self.endRemoveRows()

    def columnCount(self, parent=QModelIndex()):
        return 1

    def rowCount(self, parent=QModelIndex()):
        if parent == QModelIndex():
            return len(self.locations)
        location = parent.internalPointer()
        if location in self.locations:
            if location not in self.branches:
                self.fetchBranches(location)
            return len(self.branches[location])
        return 0

    def index(self, row, column, parent=QModelIndex()):
        if column == 0:
            if parent == QModelIndex():
                if row < len(self.locations):
                    return self.createIndex(row, column, self.locations[row])

            if parent.parent() == QModelIndex():
                location = self.locations[parent.row()]
                if location not in self.branches:
                    self.fetchBranches(location)
                branch = self.branches[location][row]
                path = os.path.join(location, branch)
                return self.createIndex(row, column, path)

        return QModelIndex()

    def parent(self, index):
        if index.column() == 0:
            path = index.internalPointer()
            if path in self.locations:
                return QModelIndex()

            print(path)
            location, branch = os.path.split(path)
            print(path)
            # print(path, path.split('/'))
            if location in self.locations:
                row = self.locations.index(location)
                return self.createIndex(row, 0, location)

        return QModelIndex()

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return self.tr("Backups location and name")

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                path = index.internalPointer()
                if path in self.locations:
                    return path

                return os.path.basename(path)


if __name__ == '__main__':
    from PyQt5.QtCore import QCoreApplication
    app = QCoreApplication([])
    app.setApplicationName("bqup")
    app.setOrganizationDomain("cbrunet.net")
    app.setOrganizationName("cbrunet")
    model = BranchesModel()

    print(model.rowCount())
    parent = model.index(0, 0)
    print(parent.data())

    print(model.rowCount(parent))
    index = model.index(0, 0, parent)
    print(index.data())

    index = model.index(1, 0, parent)
    print(index.data())
    parent = index.parent()
    print(parent.isValid())
    print(parent.data())
