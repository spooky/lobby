def test_Mod_conflictsWith_when_there_is_a_conflict():
    from models import Mod

    m = Mod(conflicts=['a', 'b'])
    assert m.conflictsWith(['a'])


def test_Mod_conflictsWith_when_there_is_no_conflict():
    from models import Mod

    m = Mod(conflicts=['a', 'b'])
    assert m.conflictsWith(['c']) is False
