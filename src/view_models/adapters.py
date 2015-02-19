from PyQt5.QtCore import QAbstractItemModel, QModelIndex, pyqtSlot


def ListModelFor(klass):
    class ListModel(QAbstractItemModel):

        def __init__(self):
            super().__init__()
            self._items = []

            meta = klass().metaObject()

            self._roleNames = {}
            for i in range(0, meta.propertyCount()):
                self._roleNames[i] = meta.property(i).name()

        def rowCount(self, parent=QModelIndex()):
            return len(self._items)

        def columnCount(self, parent=QModelIndex()):
            return 1

        def parent(self, index):
            return QModelIndex()

        def roleNames(self):
            return self._roleNames

        def data(self, index, role):
            item = self._items[index.row()]
            return item.property(self._roleNames[role])

        def index(self, row, column=0, parent=QModelIndex()):
            return self.createIndex(row, column, parent)

        def append(self, item):
            index = self.rowCount()
            self.beginInsertRows(QModelIndex(), index, index)
            self._items.append(item)
            self.endInsertRows()

        def update(self, index, item):
            self._items[index] = item
            self.dataChanged.emit(self.index(index), self.index(index))

        def remove(self, item):
            index = self._items.index(item)
            self.beginRemoveRows(QModelIndex(), index, index)
            self._items.remove(item)
            self.endRemoveRows()

        @pyqtSlot(int, str, str)
        def setProperty(self, index, prop, value):
            item = self._items[index]
            item.setProperty(prop, value)

    return ListModel
