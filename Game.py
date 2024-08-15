from math import inf, fabs
from random import randint
from copy import deepcopy
from Player import Player


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
		self.roll_total = 0

		# Create Players
		self.player_id = 0
		self.tournament_id = 0
		self.player_count = player_count
		self.remaining_players = player_count
		self.percent_remaining_players = 1.0
		self.players = []
		self.past_players = []
		for player in range(player_count):
			self.players.append(Player(f"{self.tournament_id}-{self.player_id}"))
			self.player_id += 1

	# GAME LOGIC METHODS
	def bankable(self):
		return self.roll_num > self.STARTER_ROUNDS

	def roll_dice(self):
		round_over = False
		# Roll Dice
		dice0 = randint(1, 6)
		dice1 = randint(1, 6)
		doubles = dice0 == dice1
		self.roll_total = dice0 + dice1

		if doubles:
			self.rolls_since_double = 0
		else:
			self.rolls_since_double += 1

		# Calculate similarity to seven
		self.last_roll_similarity_to_seven = fabs(abs(self.roll_total - 7) / 7 - 1)

		# Update running point total and check to see if round ends
		if self.roll_num < self.STARTER_ROUNDS:
			if self.roll_total == 7:
				self.running_point_total += 70
			else:
				self.running_point_total += self.roll_total
		else:
			if self.roll_total == 7:
				self.best_possible_score += self.running_point_total
				self.best_round_score = self.running_point_total
				self.running_point_total = 0
				round_over = True
			elif doubles:
				self.running_point_total *= 2
			else:
				self.running_point_total += self.roll_total

		self.roll_num += 1

		return round_over

	# GAME METHODS
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

	# ROUND METHODS
	def play_round(self):
		round_over = False
		while not round_over:
			round_over = self.roll_dice() or self.remaining_players == 0
			if self.bankable() and not round_over:
				self.ask_players_about_banking()

		# reset bank-ability and other statistics
		self.reset_bank_ability()
		self.adjust_bitterness()
		self.adjust_player_ranking()

	def ask_players_about_banking(self):
		for player in self.players:
			if not player.banked and player.decide_to_bank(self.running_point_total, self.percent_rounds_complete,
														   self.roll_num):
				self.remaining_players -= 1
				self.percent_remaining_players = self.remaining_players / self.player_count

	def reset_bank_ability(self):
		for player in self.players:
			player.banked = False

	# SCORE METHODS
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

	def median_game_score(self):
		sorted_players = sorted(self.players, key=lambda y: y.game_score)

		return sorted_players[int(self.player_count / 2)].game_score

	def create_random_player(self):
		# Gives a new Player
		new_player = Player(f"{self.tournament_id}-{self.player_id}")
		self.player_id += 1

		return new_player

	# INPUT NEURONS/FITNESS METHODS
	def adjust_players_fitness(self):

		# Sort players by game score and then assign them a genetic score by using that to give them a linear score +
		self.players = reversed(sorted(self.players, key=lambda y: y.game_score, ))


		for placement, player in enumerate(self.players):
			# score adjusted for player count as larger player count leads to higher scores
			player.fitness += int((placement + 1 )/ self.player_count * 100)

	def clear_fitness_scores(self):
		# Clears genetic scores for players
		for player in self.players:
			player.fitness = 0

	def clear_bitterness(self):
		for player in self.players:
			player.bitterness = 0
			player.bitterness_memories = []

	def adjust_bitterness(self):
		for player in self.players:
			# add memory
			player.record_memory(abs(player.banked_score - self.best_possible_score))
			player.calculate_bitterness()

	def adjust_player_ranking(self):
		self.players = sorted(self.players, key=lambda y: y.game_score)

		for place_ment, player in enumerate(self.players):
			player.score_ranking = place_ment / self.player_count

	# TRAINING/Tournament
	def run_tournament(self):

		# Check to see if there are 50 players and create new players if necessary
		if self.player_count < 50:
			missing_players = 50 - self.player_count
			for _ in range(missing_players):
				self.create_random_player()

		# Play Tournament
		for game_round in range(4):
			self.play_game()
			self.adjust_players_fitness()
			self.players = sorted(self.players, key=lambda y: y.fitness, )
			# trim bottom 10
			self.players = self.players[:-10]
			self.player_count -= 10
			self.reset_game()

		# Now that 10 remain play one last game determine final rankings
		self.play_game()
		self.players = sorted(self.players, key=lambda y: y.fitness, )
		# adjust player rolling queue
		self.past_players.insert(0, self.players[5:])

		if len(self.past_players) >= 11:
			self.past_players.pop(10)

		self.tournament_id += 1
		self.player_id = 0

	def generate_new_tournament_players(self):
		next_tournament_players = self.players[10:]

		self.players = sorted(self.players, key=lambda y: y.fitness, )

		top_five = deepcopy(self.players[:5])

		# Cross over top five
		descendants = []
		for i in range(len(top_five)):  # 5 choose 2 grouping
			for j in range(i, 5):
				if i != j:
					# Repeat 3 times for variety
					for _ in range(3):
						descendants.extend(self.cross_over(top_five[i], top_five[j]))

		# Mutate Descendants
		for descendant in descendants:
			descendant.network.mutate_network()

		next_tournament_players.extend(descendants)
		# Fetch players from previous rounds

		# 5 from 3 rounds ago
		if len(self.past_players) >= 3:
			next_tournament_players.extend(self.past_players[2])
		# 3 from 5 rounds ago
		if len(self.past_players) >= 5:
			next_tournament_players.extend(self.past_players[4][3:])
		# 2 from 10 rounds ago
		if len(self.past_players) >= 10:
			next_tournament_players.extend(self.past_players[3])

		self.clear_fitness_scores()

	def cross_over(self, parent0, parent1):
		# Given 2 Players cross over there neural networks

		child = deepcopy(parent0)  # To save time copy parent and then modify network
		child.cross_over(parent0, parent1)
		return child
