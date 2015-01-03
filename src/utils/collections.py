class LocalContainer():

    def __init__(self, paths=[], factory=lambda k, p: None):
        self._paths = paths
        self._factory = factory

    def __getitem__(self, k):
        import os.path

        for p in self._paths:
            item_path = os.path.join(p, k)
            if os.path.exists(item_path):
                return self._factory(k, item_path)

        raise KeyError(k)


class RemoteContainer():

    def __init__(self, paths=[], factory=lambda k, p: None):
        self._paths = paths
        self._factory = factory

    def __getitem__(self, k):
        raise KeyError(k)


class Storage():

    def __init__(self, containers=[]):
        self._containers = containers

    def __getitem__(self, k):
        item = None
        for c in self._containers:
            try:
                item = c[k]
            except KeyError:
                continue

        if item is not None:
            return item
        else:
            raise KeyError(k)
