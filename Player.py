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
		self.score_ranking = 1
		self.bitterness = 0
		self.bitterness_memories = []

		# NEURAL NET
		self.network = NeuralNetwork(4, [4, 4, 2])

	def dummy_decide_to_bank(self, running_point_total, percent_rounds_completed):
		# FILLER FUNCTION JUST USED TO SIMULATE GAMES WHILE THERE IS NO AI
		self.banked = randint(0, self.id) == 0
		if self.banked:
			self.banked_score = running_point_total

		return self.banked

	def decide_to_bank(self, running_point_total, percent_rounds_completed, roll_num):

		inputs = [running_point_total, percent_rounds_completed, roll_num, self.score_ranking]

		# Calculate output
		self.network.calculate_output(inputs)

		# if output 0 don't bank, 1 bank
		if self.network.select_action() == 1:
			self.banked = True
			self.banked_score = running_point_total
			self.fitness += running_point_total

		return self.banked

	def __str__(self):
		return f"|{self.id.__str__().center(3, " ")}|{self.game_score.__str__().center(7, " ")}|"

	def record_memory(self, points_missed_out):
		self.bitterness_memories.insert(0, points_missed_out)

	def calculate_bitterness(self):
		# I tried to shape this like a human memory by having past rounds count progressively less
		self.bitterness = 0
		for rounds_ago, bitterness in enumerate(self.bitterness_memories):
			self.bitterness += bitterness / (rounds_ago + 1)

	def cross_over(self, parent0, parent1):
		# Merges 2 neural networks
		self.network.cross_over(parent0.network, parent1.network)
