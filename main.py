from math import inf
from random import randint


def simulate_dummy_games():
	for player_count in range(1, 101):
		print(player_count)
		for x in range(1000):
			dummy_game = Game(player_count, 10)
			dummy_game.play_game()
			dummy_game.save_score_to_file()


class Game:
	def __init__(self, player_count, total_round):
		self.running_point_total = 0

		self.round_num = 0
		self.total_rounds = total_round

		self.roll_num = 0
		self.rolls_since_double = inf

		self.STARTER_ROUNDS = 3

		# Create Players
		self.player_count = player_count
		self.remaining_players = player_count
		self.players = []
		for player in range(player_count):
			self.players.append(Player(player))

	def bankable(self):
		return self.roll_num > self.STARTER_ROUNDS

	def roll_dice(self):
		round_over = False
		# Roll Dice
		dice0 = randint(1, 6)
		dice1 = randint(1, 6)
		doubles = dice0 == dice1
		total = dice0 + dice1

		# print(f"{self.roll_num}: {total}, ", end='')
		# if doubles:
		# 	print("doubles", end='')

		# UPDATE self.rolls_since_double
		if doubles:
			self.rolls_since_double = 0
		else:
			self.rolls_since_double += 1

		# Update running point total and check to see if round ends
		if self.roll_num < self.STARTER_ROUNDS:
			if total == 7:
				self.running_point_total += 70
			else:
				self.running_point_total += total
		else:
			if total == 7:
				self.running_point_total = 0
				round_over = True
			elif doubles:
				self.running_point_total *= 2
			else:
				self.running_point_total += total

		self.roll_num += 1

		return round_over

	def adjust_players_genetic_scores(self):

		# Sort players by game score and then assign them a genetic score by using that to give the a linear score +
		self.players = sorted(bank.players, key=lambda y: y.game_score, )

		for placement, player in iter(self.players):
			# score adjusted for player count as larger player count leads to higher scores
			player.score += placement/self.player_count * 100

	def median_game_score(self):
		sorted_players = sorted(self.players, key=lambda x: x.game_score)

		return sorted_players[int(self.player_count / 2)].game_score

	def play_game(self):
		for game_round in range(self.total_rounds):
			self.play_round()

			self.round_num += 1

			# reset round info
			self.remaining_players = self.player_count
			self.roll_num = 0
			self.rolls_since_double = 0

	def average_game_score(self):
		# returns the average game score

		average_score = 0
		for player in self.players:
			average_score += player.game_score
		average_score /= self.player_count

		return average_score

	def save_score_to_file(self):
		with open("dummy_player_simulated_games.csv", 'a') as f:
			f.write(f"{self.player_count},{self.median_game_score()},\n")

	def print_score_card(self):
		for player in self.players:
			print(player)

	def play_round(self):
		round_over = False
		while not round_over:
			round_over = self.roll_dice() or self.remaining_players == 0
			if self.bankable() and not round_over:
				self.ask_players_about_banking()


		# reset bank-ability
		for player in self.players:
			player.banked = False

	def ask_players_about_banking(self):
		for player in self.players:
			if not player.banked and player.dummy_decide_to_bank():
				player.game_score += self.running_point_total
				self.remaining_players -= 1


class Player:
	def __init__(self, player_id):
		self.score = 0
		self.game_score = 0
		self.banked = False
		self.id = player_id

	def dummy_decide_to_bank(self):
		# FILLER FUNCTION JUST USED TO SIMULATE GAMES WHILE THERE IS NO AI
		self.banked = randint(0, self.id) == 0

		return self.banked

	def __str__(self):
		return f"|{self.id.__str__().center(3, " ")}|{self.game_score.__str__().center(7, " ")}|"

	def run_tournament(self):
		# Starts off with N players and plays a few games to reduce the affects of chance then removes the worst X
		# players and repeats until there are Y remaining
		pass


if __name__ == '__main__':
	bank = Game(10, 10)
	for x in range(5):
		bank.play_game()

		bank.print_score_card()
		print("--------"*5)
