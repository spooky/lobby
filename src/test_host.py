import sys
from PyQt5.QtCore import QCoreApplication
from session import LobbyServerContext, GameSession, AuthService, LOBBY_HOST, LOBBY_PORT


def login(login, password):
    import hashlib
    password = hashlib.sha256(password.encode()).hexdigest()
    return AuthService.Login(login, password)


def init_context(app, session_id):
    ctx = LobbyServerContext('ws://{}:{}/notify/ws'.format(LOBBY_HOST, LOBBY_PORT), app)

    def on_reconnected():
        ctx.sendNotify('subscribe', 'games')

        if session_id:
            ctx.sendMessage('auth', 'login', session_id)

    def on_eventReceived(event_id, args):
        print(event_id, args)

    def on_messageReceived(subsystem, command, args):
        print(subsystem, command, args)

    ctx.reconnected.connect(on_reconnected)
    ctx.eventReceived.connect(on_eventReceived)
    ctx.messageReceived.connect(on_messageReceived)
    ctx.start()

    return ctx


def main():
    app = QCoreApplication(sys.argv)
    user = 'spooky'
    password = '???'
    response = login(user, password)

    def on_done(body):
        print(body)

        lobby_ctx = init_context(app, body['session_id'])

        sess = GameSession(app)

        sess.addArg('showlog')
        sess.addArg('mean', 1000)
        sess.addArg('deviation', 0)
        sess.addArg('windowed', 1024, 768)
        sess.addArg('init', 'init_test.lua')

        sess.setTitle('test')
        sess.setMap('scmp_009')
        sess.setLocalPlayer(user, body['user_id'])

        sess.setFAFConnection(lobby_ctx)
        sess.start()

    response.done.connect(on_done)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
