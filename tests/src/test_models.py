def test_Mod_conflicts_with_when_there_is_a_conflict():
    from models import Mod

    m = Mod(conflicts=['a', 'b'])
    assert m.conflicts_with(['a'])


def test_Mod_conflicts_with_when_there_is_no_conflict():
    from models import Mod

    m = Mod(conflicts=['a', 'b'])
    assert m.conflicts_with(['c']) is False
