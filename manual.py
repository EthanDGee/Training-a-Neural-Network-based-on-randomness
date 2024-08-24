from Game import Game
from Player import Player
import pickle

play_again = True
player_count = int(input("Enter Human Player Count: "))
neural_network_count = int(input("Enter Neural Network Player Count: "))

game = Game(player_count+neural_network_count, 10)
game.players = []

# add the human players
for player_num in range(player_count):
	human_player = Player(input("Enter Player Name: "))
	human_player.human = True
	game.players.append(human_player)


# import the neural network players

ai_players = []

while len(ai_players) < neural_network_count:
	# grab players from file
	file_name = input("Enter file_name: ")
	file = open(file_name, 'rb')
	ai_players = pickle.load(file)
	file.close()

	#
	num_ai_players = int(input("How many players do you want to add from this file?"))
	game.players.extend(ai_players[0:num_ai_players])

while play_again:
	game.reset_game()
	game.manual_game()

	game.print_score_card()

	play_again = ("Play Again (y/n): ") == 'y'

