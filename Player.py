from NeuralNetwork import NeuralNetwork
from random import randint


class Player:
	def __init__(self, player_id: str):
		# INFO
		self.id = player_id  # tournament id - iterated id

		# FITNESS
		self.fitness = 0

		# GAME LOGIC
		self.game_score = 0
		self.banked_score = 0
		self.banked = False

		# INPUT NEURONS
		self.bitterness = 0
		self.score_ranking = 0
		self.bitterness = 0
		self.bitterness_memories = []

		# NEURAL NET
		self.network = NeuralNetwork(8, [7, 6, 4, 2])

	# GET PLAYER INFO
	def __str__(self):
		return (f"|{self.id.__str__().center(10, " ")}|"
				f"{self.fitness.__str__().center(10, " ")}|"
				f"{self.game_score.__str__().center(10, " ")}|")

	def __eq__(self, other):
		return self.fitness == other.fitness and self.id == other.id and self.network == other.network

	def get_tournament_id(self):
		return int(self.id.split('-')[0])

	def get_player_id(self):
		return int(self.id.split('-')[1])

	def set_player_id(self, tournament, player_id):
		self.id = f"{tournament}-{player_id}"

	# BANKING
	def dummy_decide_to_bank(self, running_point_total):
		# FILLER FUNCTION JUST USED TO SIMULATE GAMES WHILE THERE IS NO AI
		self.banked = randint(0, self.id) == 0
		if self.banked:
			self.banked_score = running_point_total

		return self.banked

	def decide_to_bank(self, running_point_total, percent_rounds_completed, roll_num, percent_remaining_players,
					   last_roll_similarity_to_seven, rolls_since_double):

		inputs = [running_point_total, percent_rounds_completed, roll_num, self.score_ranking,
				  percent_remaining_players, last_roll_similarity_to_seven, self.bitterness, rolls_since_double]

		# Calculate output
		self.network.calculate_output(inputs)

		# if output 0 don't bank, 1 bank
		if self.network.select_action() == 1:
			self.banked = True
			self.banked_score = running_point_total
			self.fitness += running_point_total

		return self.banked

	# PLAYER INPUTS

	def record_memory(self, points_missed_out):
		self.bitterness_memories.insert(0, points_missed_out)

	def calculate_bitterness(self):
		# I tried to shape this like a human memory by having past rounds count progressively less
		self.bitterness = 0
		for rounds_ago, bitterness in enumerate(self.bitterness_memories):
			self.bitterness += bitterness / (rounds_ago + 1)

	# TRAINING

	def cross_over(self, parent0, parent1):
		# Merges 2 neural networks
		self.network.cross_over(parent0.network, parent1.network)
