from math import inf
from random import randint


class Game:
	def __init__(self, player_count, total_round):
		self.score = 0

		self.round_num = 0
		self.total_rounds = total_round

		self.roll_num = 0
		self.rolls_since_double = inf  # can't remember pythons math.max equivalent

		self.starter_rounds = 3

		# Create Players
		self.player_count = player_count
		self.remaining_players = player_count
		self.players = []
		for player in range(player_count):
			self.players.append(Player(player))

	def bankable(self):
		return self.roll_num > self.starter_rounds

	def roll_dice(self):
		round_over = False
		# Roll Dice
		dice0 = randint(1, 6)
		dice1 = randint(1, 6)
		doubles = dice0 == dice1
		total = dice0 + dice1

		print(f"{self.roll_num}: {total}, ", end='')
		if doubles:
			print("doubles", end='')

		# UPDATE self.rolls_since_double
		if doubles:
			self.rolls_since_double = 0
		else:
			self.rolls_since_double += 1

		# Update score and check to see if round ends
		if self.roll_num < self.starter_rounds:
			if total == 7:
				self.score += 70
			else:
				self.score += total
		else:
			if total == 7:
				self.score = 0
				round_over = True
			elif doubles:
				self.score *= 2
			else:
				self.score += total

		print(f"\nNew Score: {self.score}")
		self.roll_num += 1

		return round_over

	def adjust_players_genetic_scores(self):
		for player in self.players:
			# score adjusted for player count as larger player count leads to higher scores
			player.score += int (player.game_score / self.player_count)
	def play_game(self):
		for game_round in range(self.total_rounds):
			self.play_round()

			self.round_num += 1

			# reset round info
			self.remaining_players = self.player_count
			self.roll_num = 0
			self.rolls_since_double = 0

		# Print Scorecard
		for player in self.players:
			print(player)

	def print_score_card(self):
		for player in self.players:
			print(player)

	def play_round(self):
		round_over = False
		while not round_over:
			round_over = self.roll_dice() or self.remaining_players == 0
			if self.bankable() and not round_over:
				self.ask_players_about_banking()
		print("-_-_-_" * 6)
		print(f"ROUND {self.round_num} OVER")
		print("-_-_-_" * 6)

		# reset bank-ability
		for player in self.players:
			player.banked = False

	def ask_players_about_banking(self):
		for player in self.players:
			if not player.banked and player.decide_to_bank():
				player.game_score += self.score
				self.remaining_players -= 1


class Player:
	def __init__(self, player_id):
		self.score = 0
		self.game_score = 0
		self.banked = False
		self.id = player_id
		self.times_banked = 0

	def decide_to_bank(self):
		# 	if input(f"{self.id}: BANK?\n") == 'y':
		# 		self.banked = True
		self.banked = randint(0, 3) == 2
		if self.banked:
			print(f"{self.id} banked.")
			self.times_banked += 1
		return self.banked

	def __str__(self):
		return (f"|{self.id.__str__().center(3, " ")}| {self.game_score.__str__().center(7, " ")} | "
				f"{self.times_banked.__str__().center(3, " ")}|")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	new_game = Game(10, 10)
	new_game.play_game()
