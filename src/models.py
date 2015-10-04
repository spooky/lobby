from collections import OrderedDict
from PyQt5.QtCore import QObject


class Map(QObject):

    def __init__(self, code=None, name=None, description=None, version=None, slots=0, size=[0, 0], previewSmall=None, previewBig=None, parent=None):
        super().__init__(parent)

        self.code = code
        self.name = name or code
        self.description = description
        self.version = version
        self.slots = slots
        self.size = size
        self.previewSmall = previewSmall
        self.previewBig = previewBig

    def __str__(self):
        return {'code': self.code, 'version': self.version}.__str__()

    def __lt__(self, other):
        return self.name < other.name


class Mod(QObject):
    FEATURED = []

    def __init__(self, uid=None, name=None, description=None, author=None, version=None, icon=None, uiOnly=False, conflicts=None, parent=None):
        super().__init__(parent)

        self.uid = uid
        self.name = name
        self.description = description
        self.author = author
        self.version = version
        self.icon = icon
        self.uiOnly = uiOnly
        self.conflicts = conflicts or []

    def __str__(self):
        return {'uid': self.uid, 'name': self.name, 'version': self.version}.__str__()

    def __le__(self, other):
        return self.name <= other.name

    def conflictsWith(self, other):
        return len(set(self.conflicts).intersection(other)) > 0


class FeaturedMod(Mod):
    # cause I have no idea where & how to get the info about these...
    ALL = OrderedDict([
        ('E994FF70-B446-4217-A42F-7F520D061868', Mod(uid='E994FF70-B446-4217-A42F-7F520D061868', name='FAF (beta)')),
        ('BDEB63A2-C7A8-4AD0-B318-6BD5EDE8D429', Mod(uid='BDEB63A2-C7A8-4AD0-B318-6BD5EDE8D429', name='FAF')),
        ('9071A3E3-5ECC-436B-B26F-5C4C91056229', Mod(uid='9071A3E3-5ECC-436B-B26F-5C4C91056229', name='Blackops')),
        ('8A2ABAE6-E0AB-43A1-AEC9-1213636C6C84', Mod(uid='8A2ABAE6-E0AB-43A1-AEC9-1213636C6C84', name='Cyvilians Defense')),
        ('DE723BC3-1CD2-4D64-9A76-D98E836E81DE', Mod(uid='DE723BC3-1CD2-4D64-9A76-D98E836E81DE', name='Claustrophobia')),
        ('3374A7F6-E6A8-425B-939B-70CC952F9021', Mod(uid='3374A7F6-E6A8-425B-939B-70CC952F9021', name='Diamond')),
        ('939076B4-FDD8-4483-95E5-705F2CCF56A4', Mod(uid='939076B4-FDD8-4483-95E5-705F2CCF56A4', name='King of the Hill')),
        ('2A3E2E9F-F428-45A6-81BB-5AB9C33A863E', Mod(uid='2A3E2E9F-F428-45A6-81BB-5AB9C33A863E', name='LABwars')),
        ('02D2F98F-C59A-449F-9CB7-96B47228B15F', Mod(uid='02D2F98F-C59A-449F-9CB7-96B47228B15F', name='Murder Party')),
        ('6968AC32-26DA-4BB1-81DD-C0D843134E7E', Mod(uid='6968AC32-26DA-4BB1-81DD-C0D843134E7E', name='The Nomads')),
        ('CA94AF6B-B25A-48C1-8F71-5B33C2F05ED6', Mod(uid='CA94AF6B-B25A-48C1-8F71-5B33C2F05ED6', name='Phantom-X')),
        ('C646605E-D231-49E6-8B0D-0B860F00A17F', Mod(uid='C646605E-D231-49E6-8B0D-0B860F00A17F', name='Supreme Destruction')),
        ('0AD29712-9378-4762-912F-BAE516C2BDBC', Mod(uid='0AD29712-9378-4762-912F-BAE516C2BDBC', name='Vanilla')),
        ('146B3A7D-ECCE-4D16-A100-FCFEAB0F2678', Mod(uid='146B3A7D-ECCE-4D16-A100-FCFEAB0F2678', name='Xtreme Wars'))
    ])
