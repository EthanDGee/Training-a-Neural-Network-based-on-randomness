import unittest
from main import Player, Game, NeuralNetwork
from copy import deepcopy
from random import randint


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

		game.adjust_players_genetic_scores()

		for x, player in iter(game.players):
			self.assertEqual(player.score, calculated_fitness[x])

	def test_neuron_output(self):

		# TEST 1
		inputs = [5, 3, 4]
		weights = [0.5, 0.5, 1]
		bias = 2
		test_neuron = NeuralNetwork.Neuron(3, bias, inputs, weights)
		test_neuron.calculate_output()
		self.assertEqual(0.999999887465, test_neuron.output)

		# TEST 2
		inputs = [1, .5, -2]
		weights = [1, -0.5, 1]
		bias = 4
		test_neuron = NeuralNetwork.Neuron(3, bias, inputs, weights)
		test_neuron.calculate_output()
		self.assertEqual(0.995929862284, test_neuron.output)

		# TEST 3
		inputs = [1200, 3, 1]
		weights = [0.01, 0.5, -0.3]
		bias = -5
		test_neuron = NeuralNetwork.Neuron(3, bias, inputs, weights)
		test_neuron.calculate_output()
		self.assertEqual(0.999999924565, test_neuron.output)


if __name__ == '__main__':
	unittest.main()
