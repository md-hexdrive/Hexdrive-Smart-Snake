import os
import random

import cherrypy

import behaviour
import process_board

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""

num_games = 0
victories = 0
losses = 0

class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "md-hexdrive",  # My Battlesnake Username
            #"color": "#d65601",  # Cool orange colour
            "color": "#079b31",  # Cool darker green colour
            "head": "shac-tiger-king",  # Lion-king head
            "tail": "bolt",  # Lightning-bolt tail
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        # TODO: Use this function to decide how your snake is going to look on the board.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        # TODO: Use the information in cherrypy.request.json to decide your next move.
        data = cherrypy.request.json

        move = behaviour.find_best_move(data)
        turn = data['turn']
        print(f"MOVE: {move},", f"TURN #: {turn}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json
        global num_games
        global victories
        global losses

        print("END")
        
        num_games += 1
        if len(data['board']['snakes']) > 0:
            print("Winner:", data['board']['snakes'][0]['name'])
        if data['you'] in data['board']['snakes']:
            print("You Won!!!")
            victories += 1
        else:
            print("You Lost")
            losses += 1
        
        print("Total Games:", num_games)
        print("Victories:", victories)
        print("defeats:", losses)
        
        print("\n\nPercent Won:", int((victories / num_games) * 100))
        print("\nPercent Lost:", int((losses / num_games) * 100))
        #cherrypy.engine.exit()
        return "ok"


if __name__ == "__main__":

    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
