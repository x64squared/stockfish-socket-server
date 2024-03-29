from flask import Flask
from flask_sock import Sock
from stockfish_socket_server.models import StockfishSocketEmitter

app = Flask(__name__)
socket = Sock(app)

@socket.route('/senduci')
def process_uci(ws):
    """
    Route for sending and handling uci engine commands
    :param ws: Websocket connection
    :return: None
    """
    stockfish_socket_emitter = StockfishSocketEmitter(
        stockfish_path=app.config.get('stockfish_path')
    )
    stockfish_socket_emitter.start(ws)
    while True:
        text = ws.receive()
        if text == 'quit':
            stockfish_socket_emitter.stop()
        else:
            stockfish_socket_emitter.send_uci(text)
