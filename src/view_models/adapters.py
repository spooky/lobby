from PyQt5.QtCore import QAbstractItemModel, QAbstractListModel, QModelIndex, QObject, QVariant, pyqtSlot, pyqtProperty, pyqtSignal, pyqtWrapperType


def ListModelFor(klass):
    class ListModel(QAbstractItemModel):

        def __init__(self, parent=None):
            super().__init__(parent)
            self._items = []

            meta = klass().metaObject()

            self._roleNames = {}
            for i in range(0, meta.propertyCount()):
                self._roleNames[i] = meta.property(i).name().encode()

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


class notifyableProperty:

    '''
        Just a placeholder, it gets replaced with pyqtProperty
        when creating the object. Used to customise signal name.
    '''

    def __init__(self, propertyType, signalName=None):
        self.propertyType = propertyType
        self.signalName = signalName


class notifyablePropertyWrapperType(pyqtWrapperType):

    ''' Generates a *_changed signal for each pyqtProperty found for a class '''

    def __new__(meta, name, bases, dct):

        def createNotifyableProperty(propName, propType, notify, notifyName):
            '''
                Create pyqtProperty object with value captured in the closure
                and a 'notify' signal attached.

                You need to pass both:
                    - unbound signal, because pyqtProperty needs it
                    - signal name to allow setter to find the *bound* signal
                      and emit it.
            '''

            def getter(self):
                return getattr(self, '__' + propName)

            def setter(self, value):
                setattr(self, '__' + propName, value)
                getattr(self, notifyName).emit(value)

            return pyqtProperty(type=propType, fget=getter, fset=setter, notify=notify)

        # don't touch attributes other than notifyableProperties
        properties = list(
            filter(
                lambda i: isinstance(i[1], notifyableProperty),
                dct.items()
            )
        )

        for propertyName, p in properties:
            signalName = p.signalName or propertyName + '_changed'
            signal = pyqtSignal(p.propertyType, name=signalName)

            # create dedicated signal for each property
            dct[signalName] = signal

            # create property backing field
            dct['__' + propertyName] = None

            # substitute notifyableProperty placeholder with real pyqtProperty
            dct[propertyName] = createNotifyableProperty(propertyName, p.propertyType, signal, signalName)

        return super().__new__(meta, name, bases, dct)


class NotifyablePropertyObject(QObject, metaclass=notifyablePropertyWrapperType):

    ''' Base class for model objects. This class uses PropertyChangeSignalMeta to generate signals for each pyqtProperty found in a class '''

    pass


class Selectable(NotifyablePropertyObject):

    name = notifyableProperty(str)
    selected = notifyableProperty(bool)

    def __init__(self, item, nameExtractor=None):
        super().__init__()
        self._item = item
        self.selected = False
        self.name = (nameExtractor or (lambda x: str(x)))(item)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    @pyqtSlot()
    def toggleSelected(self):
        self.selected = not self.selected


class SelectionList(QAbstractListModel, NotifyablePropertyObject):

    currentIndex = notifyableProperty(int)

    def __init__(self, items=None, multiple=False, itemNameExtractor=None, parent=None):
        super().__init__()
        self.currentIndex = -1
        self.multiple = multiple
        self._items = [Selectable(i, self._nameExtractor) for i in (items or [])]
        self._nameExtractor = itemNameExtractor or self.__defaultNameExtractor

    def __getitem__(self, key):
        return self._items[key]

    def __defaultNameExtractor(self, x):
        return x.name if hasattr(x, 'name') else x.__str__()

    def roleNames(self):
        return {0: b'item', 1: b'name'}

    def rowCount(self, parent=QModelIndex()):
        return len(self._items)

    def data(self, index, role):
        if index.isValid():
            if role == 0:
                return self._items[index.row()]
            if role == 1:
                return self._items[index.row()].name

    def append(self, item, selected=False):
        index = len(self._items)
        self.beginInsertRows(QModelIndex(), index, index)

        e = Selectable(item, self._nameExtractor)
        e.selected = selected
        self._items.append(e)

        self.endInsertRows()

    def remove(self, item):
        e = Selectable(item, self._nameExtractor)

        index = self._items.index(e)
        self.beginRemoveRows(QModelIndex(), index, index)

        self._items.remove(e)

        self.endRemoveRows()

    @pyqtSlot(result=QVariant)
    def getSelectedIndex(self):
        s = self._selections()
        if self.multiple:
            [self._items.index(i) for i in s]
        elif len(s) > 0:
            return self._items.index(s[0])

    def _selections(self):
        return [x for x in self._items if x.selected]

    def selected(self):
        s = [x._item for x in self._items if x.selected]
        return s if self.multiple else s[0] if len(s) > 0 else None

    @pyqtSlot(int)
    @pyqtSlot(int, bool)
    def setSelected(self, index, selected=True):
        if not self.multiple:
            for s in self._selections()[:]:
                s.selected = False

        if len(self._items) > index:
            self._items[index].selected = selected
            self.currentIndex = index
