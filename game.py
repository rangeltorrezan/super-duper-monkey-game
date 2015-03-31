from flask import Flask
import redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World Rangel!"

@app.route("/start/<table_name>")
def open_game(table_name):
    redis.sadd("games", table_name)
    redis.set(table_name+":current_player", 1)
    return "opened! player1 will start...coz i want"

@app.route("/games")
def games_opened():
    return str(redis.smembers("games"))

@app.route("/games/<table_name>")
def game(table_name):
    if redis.sismember("games", table_name):
        if redis.get(table_name+":current_player") is None:
            return "lolool...bad game...lolllololo....kill it!"
        return "is running"
    return "is not"

@app.route("/games/<table_name>/sort_word")
def sort_word(table_name):
    if not redis.sismember("games", table_name):
        raise LoLException('noooo!')
    redis.set(table_name+":current_word", "batata")
    redis.expire(table_name+":current_word", 10)
    return "i've sorted! yahoo"

@app.route("/games/<table_name>/<int:player>/current_word")
def current_word(table_name, player):
    if not redis.sismember("games", table_name):
        raise LoLException('noooo!')
    current_player = redis.get(table_name+":current_player")
    if player is not None:
        if player == int(redis.get(table_name+":current_player")):
            return "lololololol...stop cheating"
    word=redis.get(table_name+":current_word")
    print word
    if word is None:
        raise Exception("word expired")

@app.route("/games/<table_name>/<int:player>/guess/<guessed_word>")
def guess_word(table_name, player, guessed_word):
    if player != int(redis.get(table_name+":current_player")):
        return "lololololol...stop talking"
    word=None
    try:
        word=current_word(table_name, None)
    except:
        return "time is over!!!!! you loooooooooooooooooooooose"
    current_player = redis.get(table_name+":current_player")
    print type(current_player)
    if guessed_word == word:
        return "win"
    return "try again"

if __name__ == "__main__":
    app.run(debug=True)
