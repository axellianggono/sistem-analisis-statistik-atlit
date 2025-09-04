from flask import Blueprint, request, render_template
from .players import PlayerRepository


urls = Blueprint('urls', __name__)

@urls.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@urls.route('/players', methods=['GET'])
def fetch():
    return render_template("players.html", datas=PlayerRepository.paginate(page=int(request.args.get('page', 1)), per_page=5))

@urls.route('/player/<string:name>', methods=['GET'])
def get(name):
    return render_template("player.html", player=PlayerRepository.find_by_name(name)['player'], next=PlayerRepository.find_by_name(name)['next'], prev=PlayerRepository.find_by_name(name)['prev'])

@urls.route('/compare', methods=['GET'])
def compare():
    player1 = request.args.get('player1')
    player2 = request.args.get('player2')

    if not player1 or not player2:
        return render_template("compare.html", player1=None, player2=None)
    
    p1 = PlayerRepository.find_by_name(player1)['player']
    p2 = PlayerRepository.find_by_name(player2)['player']

    return render_template("compare.html", player1=p1, player2=p2, next1=PlayerRepository.find_by_name(player1)['next'], prev1=PlayerRepository.find_by_name(player1)['prev'], next2=PlayerRepository.find_by_name(player2)['next'], prev2=PlayerRepository.find_by_name(player2)['prev'])
