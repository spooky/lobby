from PyQt5.QtCore import QAbstractItemModel, QAbstractListModel, QModelIndex, QObject, QVariant, pyqtSlot, pyqtProperty, pyqtSignal, pyqtWrapperType


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


class SelectionList(QAbstractListModel):

    def __init__(self, multiple=False, parent=None):
        super().__init__(parent)
        self.multiple = multiple
        self._items = []
        self._selected = set()
        self._roleNames = {1: 'name'}  # TODO: do the thing...

    def roleNames(self):
        return self._roleNames

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role):
        item = self._items[index.row()]
        return getattr(item, self._roleNames[role])

    def append(self, item, selected=False):
        index = len(self._items)
        self.beginInsertRows(QModelIndex(), index, index)
        self._items.append(item)
        if selected:
            self._selected.add(index)
        self.endInsertRows()

    def remove(self, item):
        index = self._items.index(item)
        self.beginRemoveRows(QModelIndex(), index, index)
        self._items.remove(item)
        self.endRemoveRows()

    @pyqtSlot(int)
    @pyqtSlot(int, bool)
    def setSelected(self, index, selected=True):
        if selected:
            if not self.multiple:
                self._selected.clear()

            self._selected.add(index)
        else:
            self._selected.discard(index)

    @pyqtSlot(int, result=bool)
    def isSelected(self, index):
        return index in self._selected

    @pyqtSlot(result=QVariant)
    def getSelected(self):
        s = [self._items[i] for i in self._selected]
        return s if self.multiple else s[0]

    @pyqtSlot(result=QVariant)
    def getSelectedIndex(self):
        s = list(self._selected)
        return s if self.multiple else s[0] if len(s) > 0 else None

    @pyqtSlot()
    def clearSelection(self):
        self.beginRemoveRows(QModelIndex(), 0, 0)
        self._selected.clear()
        self.endRemoveRows()


class notifyableProperty:

    """
        Just a placeholder, it gets replaced with pyqtProperty
        when creating the object. Used to customise signal name.
    """

    def __init__(self, property_type, signal_name=None):
        self.property_type = property_type
        self.signal_name = signal_name


class notifyablePropertyWrapperType(pyqtWrapperType):

    ''' Generates a *_changed signal for each pyqtProperty found for a class '''

    def __new__(meta, name, bases, dct):

        def notifyable_property(prop_name, prop_type, notify, notify_name):
            """
                Create pyqtProperty object with value captured in the closure
                and a 'notify' signal attached.

                You need to pass both:
                    - unbound signal, because pyqtProperty needs it
                    - signal name to allow setter to find the *bound* signal
                      and emit it.
            """

            def getter(self):
                return getattr(self, '__' + prop_name)

            def setter(self, value):
                setattr(self, '__' + prop_name, value)
                getattr(self, notify_name).emit(value)

            return pyqtProperty(type=prop_type, fget=getter, fset=setter, notify=notify)

        # don't touch attributes other than notifyableProperties
        properties = list(
            filter(
                lambda i: isinstance(i[1], notifyableProperty),
                dct.items()
            )
        )

        for property_name, p in properties:
            signal_name = p.signal_name or property_name + '_changed'
            signal = pyqtSignal(p.property_type, name=signal_name)

            # create dedicated signal for each property
            dct[signal_name] = signal

            # create property backing field
            dct['__' + property_name] = None

            # substitute notifyableProperty placeholder with real pyqtProperty
            dct[property_name] = notifyable_property(property_name, p.property_type, signal, signal_name)

        return super().__new__(meta, name, bases, dct)


class NotifyablePropertyObject(QObject, metaclass=notifyablePropertyWrapperType):

    ''' Base class for model objects. This class uses PropertyChangeSignalMeta to generate signals for each pyqtProperty found in a class '''

    pass
