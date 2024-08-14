from math import inf, fabs, tanh
from random import randint, choice, random
from copy import deepcopy
import numpy as np


def simulate_dummy_games():
	for player_count in range(1, 101):
		print(player_count)
		for x in range(1000):
			dummy_game = Game(player_count, 10)
			dummy_game.play_game()
			dummy_game.save_score_to_file()


class Game:
	def __init__(self, player_count, total_round):
		# SCCORE
		self.running_point_total = 0
		self.best_possible_score = 0
		self.best_round_score = 0

		# ROUND INFO
		self.round_num = 0
		self.total_rounds = total_round
		self.percent_rounds_complete = 0

		# ROLL INFO
		self.roll_num = 0
		self.rolls_since_double = inf
		self.STARTER_ROUNDS = 3
		self.last_roll_similarity_to_seven = 0

		# Create Players
		self.player_count = player_count
		self.remaining_players = player_count
		self.percent_remaining_players = 1.0
		self.players = []
		self.past_players = []
		for player in range(player_count):
			self.players.append(Player(player))

	def bankable(self):
		return self.roll_num > self.STARTER_ROUNDS

	def run_tournament(self):

		# Check to see if there are 50 players and create new players if necessary
		if self.player_count < 50:
			missing_players = 50 - self.player_count
			for _ in range(missing_players):
				self.create_random_player()

		# Play Tournament
		for game_round in range(4):
			self.play_game()
			self.adjust_players_genetic_scores()
			self.players = sorted(bank.players, key=lambda y: y.score, )
			# trim bottom 10
			self.players = self.players[:-10]
			self.player_count -= 10
			self.reset_game()

		# Now that 10 remain play one last game determine final rankings
		self.play_game()
		self.players = sorted(bank.players, key=lambda y: y.score, )
		# adjust player rolling queue
		self.past_players.insert(0, self.players[5:])

		try:
			self.past_players.pop(10)
		except:
			print("Player Queue Still Growing")

	def generate_new_tournament_players(self):
		next_tournament_players = self.players[10:]

		self.players = sorted(bank.players, key=lambda y: y.score, )

		top_five = deepcopy(self.players[:5])

		# Cross over top five
		descendants = []
		for i in range(len(top_five)):  # 5 choose 2 grouping
			for j in range(i, 5):
				if i != j:
					# Repeat 3 times for variety
					for _ in range(3):
						descendants.append(self.cross_over(top_five[i], top_five[j]))

		next_tournament_players.append(self.mutate(descendants))
		# Fetch players from previous rounds

		# 5 from 3 rounds ago
		if len(self.past_players) >= 3:
			next_tournament_players.append(self.past_players[2])
		# 3 from 5 rounds ago
		if len(self.past_players) >= 5:
			next_tournament_players.append(self.past_players[4][3:])
		# 2 from 10 rounds ago
		if len(self.past_players) >= 10:
			next_tournament_players.append(self.past_players[3])

		self.clear_genetic_scores()

	def roll_dice(self):
		round_over = False
		# Roll Dice
		dice0 = randint(1, 6)
		dice1 = randint(1, 6)
		doubles = dice0 == dice1
		total = dice0 + dice1

		if doubles:
			self.rolls_since_double = 0
		else:
			self.rolls_since_double += 1

		# Calculate similarity to seven
		self.last_roll_similarity_to_seven = fabs(abs(total - 7) / 7 - 1)

		# Update running point total and check to see if round ends
		if self.roll_num < self.STARTER_ROUNDS:
			if total == 7:
				self.running_point_total += 70
			else:
				self.running_point_total += total
		else:
			if total == 7:
				self.best_possible_score += self.running_point_total
				self.best_round_score = self.running_point_total
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
			player.score += placement / self.player_count * 100

	def adjust_plauer_ranking(self):
		self.players = reversed(sorted(self.players, key=lambda x: x.game_score))

		for place_ment, player in iter(self.players):
			player.score_ranking = place_ment / self.player_count

	def median_game_score(self):
		sorted_players = sorted(self.players, key=lambda x: x.game_score)

		return sorted_players[int(self.player_count / 2)].game_score

	def play_game(self):
		for game_round in range(self.total_rounds):
			self.play_round()

			self.round_num += 1
			self.percent_rounds_complete = self.round_num / self.total_rounds

			# reset round info
			self.remaining_players = self.player_count
			self.roll_num = 0
			self.rolls_since_double = 0

	def reset_game(self):
		self.round_num = 0
		self.percent_rounds_complete = 0
		self.clear_bitterness()

	def average_game_score(self):
		# returns the average game score

		average_score = 0
		for player in self.players:
			average_score += player.game_score
		average_score /= self.player_count

		return average_score

	def save_score_to_file(self):
		with open("simulated_games.csv", 'a') as f:
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

		# reset bank-ability and other statistics
		self.reset_bankability()
		self.adjust_bitterness()
		self.adjust_plauer_ranking()

	def reset_bankability(self):
		for player in self.players:
			player.banked = False

	def ask_players_about_banking(self):
		for player in self.players:
			if not player.banked and player.dummy_decide_to_bank():
				player.game_score += self.running_point_total
				self.remaining_players -= 1
				self.percent_remaining_players = self.remaining_players / self.player_count

	def create_random_player(self):
		pass

	def clear_genetic_scores(self):
		for player in self.players:
			player.score = 0

	def clear_bitterness(self):
		for player in self.players:
			player.bitterness = 0
			player.bitterness_memories = []

	def adjust_bitterness(self):
		for player in self.players:
			# add memory
			player.record_memory(player.banked_score - self.best_possible_score)
			player.calculate_bitterness()


class Player:
	def __init__(self, player_id):
		self.score = 0
		self.game_score = 0
		self.banked_score = 0
		self.banked = False
		self.id = player_id  # tournament id - iterated id
		self.bitterness = 0
		self.score_ranking = 1
		self.bitterness = 0
		self.bitterness_memories = []

	def dummy_decide_to_bank(self, running_point_total, percent_rounds_completed, ):
		# FILLER FUNCTION JUST USED TO SIMULATE GAMES WHILE THERE IS NO AI
		self.banked = randint(0, self.id) == 0
		if self.banked:
			self.banked_score = running_point_total

		return self.banked

	def __str__(self):
		return f"|{self.id.__str__().center(3, " ")}|{self.game_score.__str__().center(7, " ")}|"

	def record_memory(self, points_missed_out):
		self.bitterness_memories.insert(0, points_missed_out)

	def calculate_bitterness(self):
		# I tried to shape this like a human memory by having past rounds count progressively less
		self.bitterness = 0
		for rounds_ago, bitterness in iter(self.bitterness_memories):
			self.bitterness += bitterness / rounds_ago


class Neural_Network:
	def __init__(self, num_inputs, num_hidden_layers, num_outputs):
		self.num_inputs = num_inputs
		self.inputs = []
		self.num_hidden_layers = num_hidden_layers
		self.num_outputs = num_outputs
		self.outputs = []

		self.learning_rate = 0.03

	def select_output(self):
		# return ID of max output
		max_output = -inf
		max_id = 0

		for output_id, output in iter(self.outputs):
			if output > max_output:
				max_output = output
				max_id = output_id

		return max_id

	class Neuron:
		def __init__(self, num_inputs, num_weights, bias=None, inputs=None, weights=None):

			self.num_inputs = num_inputs
			self.num_weights = num_weights
			self.inputs = inputs
			self.output = 0
			self.mutation_step = 0.03

			# If empty assign random weights and biases
			if bias is None:
				bias = random()

			self.bias = bias

			if weights is None:
				weights = [random() for _ in range(num_weights)]

			self.weights = weights

		def mutate(self):
			# Adjust Bias
			self.bias += choice([-self.mutation_step, self.mutation_step])

			# Adjust Bias/Weights
			for id in range(self.num_weights):
				self.inputs[id] += choice([-self.mutation_step, self.mutation_step])
				self.weights[id] += choice([-self.mutation_step, self.mutation_step])


		def activation(self, num):
			return (tanh(num) + 1) / 2

		def calculate_output(self):
			product = 0
			for id, input in iter(self.inputs):
				product += input * self.weights[id]

			product += self.bias

			self.output = self.activation(product)

			return self.output



if __name__ == '__main__':
	bank = Game(10, 10)
	for x in range(5):
		bank.play_game()

		bank.print_score_card()
		print("--------" * 5)
