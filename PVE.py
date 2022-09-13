from abc import ABC
from random import randint


def turn_logic(difficulty: str) -> tuple[int, int]:
    if "1" in difficulty:
        row = randint(0, 2)
        column = randint(0, 2)
        return row, column
    else:
        pass


class Game:
    game_fild: list[list[str]] = [["-" for j in range(3)] for i in range(3)]
    game_objects: tuple[str] = ("X", "0")
    state: str = "draw"
    turn_number: int = 0
    players: tuple[str] = ("first player", "second player")
    game_mod: str = "1"

    def __init__(self, difficulty):
        self.game_mod = difficulty

    def turn(self) -> None:
        global player
        global ai
        if self.turn_number % 2 == 0 and ai.name == self.players[0] and self.turn_number != 9:
            ai.make_turn()
            return None
        if self.turn_number % 2 == 0 and player.name == self.players[0] and self.turn_number != 9:
            player.make_turn()
            return None
        if ai.name == self.players[1] and self.turn_number != 9:
            ai.make_turn()
            return None
        if player.name == self.players[1] and self.turn_number != 9:
            player.make_turn()
            return None


class Player(ABC):
    name: str
    state: str = "loser"

    def is_win(self, row, column, game_object) -> None:
        counter_row: int = 0
        counter_column: int = 0
        counter_main_diagonal: int = 0
        counter_secondary_diagonal: int = 0
        game_fild = Game.game_fild
        for i in range(len(Game.game_fild)):
            if game_fild[row][i] == game_object:
                counter_row += 1
            if game_fild[i][column] == game_object:
                counter_column += 1
            if game_fild[i][i] == game_object:
                counter_main_diagonal += 1
            if game_fild[i][len(Game.game_fild) - 1 - i] == game_object:
                counter_secondary_diagonal += 1
        if (counter_column == len(game_fild) or counter_row == len(game_fild) or
                counter_main_diagonal == len(game_fild) or counter_secondary_diagonal == len(game_fild)):
            self.state = "winner"
            Game.state = f"{self.name} {self.state[0:4]}'s"


class AI(Player):
    turn_number: int = randint(0, 1)
    name: str = Game.players[not turn_number == 0]
    game_object: str = Game.game_objects[not turn_number == 0]

    def make_turn(self) -> None:
        row, column = turn_logic(Game.game_mod)
        if Game.game_fild[row][column] == "-":
            Game.game_fild[row][column] = self.game_object
            Game.turn_number += 1
            print("The bot has finished his turn")
            print("=" * 255)
            print(*Game.game_fild, sep="\n")
            print("=" * 255)
            self.is_win(row, column, self.game_object)
        else:
            self.make_turn()


class HumanPlayer(Player):
    turn_number: int = not bool(AI.turn_number)
    name: str = Game.players[not turn_number == 0]
    game_object: str = Game.game_objects[not turn_number == 0]

    def make_turn(self) -> None:
        try:
            row = int(input("Type row number: "))
            column = int(input("Type column number: "))
            if Game.game_fild[row][column] == "-":
                Game.game_fild[row][column] = self.game_object
                Game.turn_number += 1
                print(*Game.game_fild, sep="\n")
                print("=" * 255)
                self.is_win(row, column, self.game_object)
            else:
                print("This place is reserved")
                self.make_turn()
        except IndexError:
            print("Incorrect value (all values must be between 0 and 2)")
            self.make_turn()
        except ValueError:
            print("Not a number")
            self.make_turn()


if __name__ == '__main__':
    print("Chose a game difficulty: ",
          "1 - Easy",
          "2 - Hard",
          sep="\n")
    game_mod = input("Type number of difficulty:")
    game = Game(game_mod)
    ai = AI()
    player = HumanPlayer()
    print("=" * 255)
    print(f"You are the {player.name}")
    print(f"Bot is the {ai.name}")
    print(f"Game Mod: {'Easy' if '1' in game.game_mod else 'Hard'}")
    print("=" * 255)
    if player.name == game.players[0]:
        print(*Game.game_fild, sep="\n")
        print("=" * 255)
    for j in range(9):
        game.turn()
        if game.state != "draw":
            print(game.state.capitalize())
            print(f"In turn: {game.turn_number}")
            break
    else:
        print(game.state.capitalize())
