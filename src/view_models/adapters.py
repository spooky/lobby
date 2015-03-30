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


class Selectable(NotifyablePropertyObject):

    name = notifyableProperty(str)
    selected = notifyableProperty(bool)

    def __init__(self, item, name_extractor=None):
        super().__init__()
        self._item = item
        self.selected = False
        self.name = (name_extractor or (lambda x: str(x)))(item)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    @pyqtSlot()
    def toggle_selected(self):
        self.selected = not self.selected


class SelectionList(QAbstractListModel, NotifyablePropertyObject):

    currentIndex = notifyableProperty(int)

    def __init__(self, items=None, multiple=False, item_name_extractor=None, parent=None):
        super().__init__()
        self.currentIndex = -1
        self.multiple = multiple
        self._items = [Selectable(i, self._name_extractor) for i in (items or [])]
        self._name_extractor = item_name_extractor

    def roleNames(self):
        return {0: 'item', 1: 'name'}

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

        e = Selectable(item, self._name_extractor)
        e.selected = selected
        self._items.append(e)

        self.endInsertRows()

    def remove(self, item):
        e = Selectable(item, self._name_extractor)

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
