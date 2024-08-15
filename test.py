import unittest
from copy import deepcopy
from random import randint
from Player import Player
from Game import Game
from NeuralNetwork import NeuralNetwork


class MyTestCase(unittest.TestCase):
	def test_rolls(self):
		game = Game(10, 10)
		possible_rolls = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
		for _ in range(10):
			game.roll_dice()
			self.assertLessEqual(game.roll_total, 12)
			self.assertGreaterEqual(game.roll_total, 2)

	def test_neuron_activation(self):
		network = NeuralNetwork(3, [4, 5, 2])
		self.assertEqual(network.Neuron.activation(5), 0.9999546021312975)
		self.assertEqual(network.Neuron.activation(-1), 0.11920292202211757)
		self.assertEqual(network.Neuron.activation(0), 0.5)

	def test_neuron_equal(self):
		for _ in range(3):
			neuron = NeuralNetwork.Neuron(randint(1, 5))
			neuron_copy = deepcopy(neuron)
			self.assertEqual(neuron, neuron_copy)

	def test_neuron_mutate(self):
		for x in range(5):
			neuron = NeuralNetwork.Neuron(3)
			mutated = deepcopy(neuron)
			mutated.mutate()
			self.assertNotEqual(neuron, mutated)

	def test_fitness_function(self):
		game = Game(3, 5)
		calculated_fitness = [100, 50, 33]
		game_scores = [1000, 300, 5]
		for x in range(len(game.players)):
			game.players[x].game_score = game_scores[x]

		game.adjust_players_fitness()

		for x, player in enumerate(game.players):
			self.assertEqual(calculated_fitness[x], player.fitness)

	def test_adjust_player_ranking(self):
		game = Game(10, 5)
		calculated_placement = [0, .1, .2, .3, .4, .5, .6, .7, .8, 0.9]
		game_scores = [1000, 900, 780, 770, 653, 450, 427, 300, 233, 21]
		for x in range(len(game.players)):
			game.players[x].game_score = game_scores[x]

		game.adjust_player_ranking()

		for x, player in enumerate(game.players):
			self.assertEqual(calculated_placement[x], player.score_ranking)

	def test_neuron_output(self):
		# TEST 0
		inputs = [1, 2, -4]
		weights = [1, 0.5, -0.25]
		bias = -3
		test_neuron = NeuralNetwork.Neuron(3, bias, inputs, weights)
		test_neuron.calculate_output()
		self.assertEqual(0.5, test_neuron.output)

		# TEST 1
		inputs = [5, 3, 4]
		weights = [0.5, 0.5, 1]
		bias = 2
		test_neuron = NeuralNetwork.Neuron(3, bias, inputs, weights)
		test_neuron.calculate_output()
		self.assertEqual(0.9999999979388463, test_neuron.output)

		# TEST 2
		inputs = [1, .5, -2]
		weights = [1, -0.5, 1]
		bias = 4
		test_neuron = NeuralNetwork.Neuron(3, bias, inputs, weights)
		test_neuron.calculate_output()
		self.assertEqual(0.9959298622841039, test_neuron.output)

		# TEST 3
		inputs = [1200, 3, 1]
		weights = [0.01, 0.5, -0.3]
		bias = -5
		test_neuron = NeuralNetwork.Neuron(3, bias, inputs, weights)
		test_neuron.calculate_output()
		self.assertEqual(0.9999999245654222, test_neuron.output)

	def test_bitterness(self):
		player = Player("0-0")
		for _ in range(10):
			player.record_memory(-10)
		player.calculate_bitterness()
		self.assertEqual(-29.289682539682538, player.bitterness)

		memories = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
		player = Player("0-1")
		for memory in memories:
			player.record_memory(memory)
		player.calculate_bitterness()
		self.assertEqual(10, player.bitterness)

		player = Player("0-2")
		memories = [-1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
		for x in memories:
			player.record_memory(x * (-1 ** x))
		player.calculate_bitterness()
		self.assertEqual(-0.6456349206349207, player.bitterness)

	def test_init_neuron(self):
		# CHECK TO SEE IF THAT THE FUNCTION WORKS
		neuron_0 = NeuralNetwork.Neuron(4)
		self.assertFalse(neuron_0 is None)
		neuron_5 = NeuralNetwork.Neuron(1)
		self.assertFalse(neuron_5 is None)
		neuron_3 = NeuralNetwork.Neuron(2)
		self.assertFalse(neuron_3 is None)
		neuron_2 = NeuralNetwork.Neuron(12)
		self.assertFalse(neuron_2 is None)

	def test_init_neural_network(self):
		# JUST A SIMPLE CHECK TO SEE THAT

		neural_network_0 = NeuralNetwork(3, [2, 4, 2, 1])
		self.assertFalse(neural_network_0 is None)
		self.assertEqual(4, len(neural_network_0.layers))

		neural_network_1 = NeuralNetwork(1, [4, 12, 3])
		self.assertFalse(neural_network_1 is None)
		self.assertEqual(3, len(neural_network_1.layers))

		neural_network_2 = NeuralNetwork(3, [2, 1, 2, 1])
		self.assertFalse(neural_network_2 is None)
		self.assertEqual(4, len(neural_network_2.layers))

		neural_network_3 = NeuralNetwork(10, [12, 4, 6, 7, 1, 6, 32, 12])
		self.assertFalse(neural_network_3 is None)
		self.assertEqual(8, len(neural_network_3.layers))

		neural_network_4 = NeuralNetwork(3, [2])
		self.assertFalse(neural_network_4 is None)
		self.assertEqual(1, len(neural_network_4.layers))


if __name__ == '__main__':
	unittest.main()
