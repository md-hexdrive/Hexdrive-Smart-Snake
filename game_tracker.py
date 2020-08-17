"""
Keep track of running games and your statistics
"""


def get_game_id(data):
    return data['game']['id']


def survived(data):
    me = data["you"]
    if me in data["board"]["snakes"]:
        return True
    else:
        return False


class Game:
    def __init__(self, data):
        self.game_id = get_game_id(data)

        self.data = data
        self.num_snakes = len(data["board"]["snakes"])
        if self.num_snakes == 1:
            self.is_solo = True
        else:
            self.is_solo = False


class GameTracker:
    def __init__(self):
        self.games = []
        self.won = 0
        self.lost = 0
        self.played = 0

    def add_game(self, data):
        game = Game(data)
        self.games.append(game)
        self.played += 1

    def __getitem__(self, data):
        key = get_game_id(data)
        for game in self.games:
            if game.game_id == key:
                return game

    def game_over(self, data):

        game = self.__getitem__(data)
        if not game.is_solo:
            if len(data['board']['snakes']) > 0:
                print("Winner:", data['board']['snakes'][0]['name'])
            else:
              print("Game ended in a draw")
            if survived(data):
                self.won += 1
                print("You Won!")
            else:
                self.lost += 1
                print("Sorry, You lost")
        else:
            print("Solo game")

        print("Total Games:", self.played)
        print("Victories:", self.won)
        print("defeats", self.lost)

        competition_games = self.won + self.lost
        if competition_games > 0:
            print("Percent Won", (self.won / (self.won + self.lost)) * 100)
            print("Percent Lost", (self.lost / (self.won + self.lost)) * 100)
