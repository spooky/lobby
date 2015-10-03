from games.models import Game


def gameFactory():

    def nextId(start=0):
        while True:
            yield start
            start += 1

    id = nextId()

    def generate():
        g = Game()
        g.id = next(id)
        g.mapCode = '3v3 Sand Box v2a'
        g.title = 'Test {}'.format(g.id)
        g.host = 'spooky'
        g.featuredMod = 'uid-faf'
        g.mods = ['921bdf63-c14a-1415-a758-42d1c231e4f4', 'EEFFA8C6-96D9-11E4-9DA1-460D1D5D46B0']
        g.slots = 6
        g.players = 4
        g.teams = [[{'name': 'crunchy', 'cc': 'pl', 'skill': 1000}, {'name': 'creamy', 'cc': 'dk', 'skill': 100}],
                   [{'name': 'cookie', 'cc': 'fi', 'skill': 1500}]]
        g.balance = 0.9

        return g

    return generate
