def test_notifyableProperty():
    from view_models.adapters import NotifyablePropertyObject, notifyableProperty

    class TestSubject(NotifyablePropertyObject):
        name = notifyableProperty(str)
        code = notifyableProperty(str, signal_name='kung_foo')

        def __init__(self, name=None, code=None, parent=None):
            super().__init__(parent)
            self.name = name
            self.code = code

            self.name_changed.connect(self.on_name_changed)

        def on_name_changed(self):
            nonlocal was_on_name_changed_called
            was_on_name_changed_called = True

    was_on_name_changed_called = False  # poor mans method call check

    t = TestSubject('first', 'second')
    q = TestSubject('not first', 'not second')

    assert t.name == 'first'
    assert t.code == 'second'
    assert hasattr(t, 'name_changed')
    assert hasattr(t, 'kung_foo')

    t.name = 'changed'
    assert t.name == 'changed'
    assert was_on_name_changed_called

    t.code = 'code_changed'
    assert t.code == 'code_changed'
