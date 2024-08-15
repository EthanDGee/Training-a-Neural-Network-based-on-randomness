from math import inf, tanh
from random import random, choice


class NeuralNetwork:
	def __init__(self, num_inputs, layer_layout):
		# Layer layout is formatted like [5,3,3] which means 3 hidden layers with the requisite amount of neurons

		self.num_inputs = num_inputs
		self.inputs = []

		self.num_outputs = layer_layout[:-1]
		self.output_layer = len(layer_layout) - 1

		self.num_layers = len(layer_layout)
		self.layers = []

		self.mutation_chance = 0.05

		# Create Random Layers
		input_numbers = [num_inputs]
		input_numbers.extend(layer_layout[:-1])
		for layer_num, neuron_amount in enumerate(layer_layout):
			# print(f"{layer_num}_{neuron_amount}")
			hidden_layer = []
			for i in range(neuron_amount):
				# print(f"{hidden_layer}")
				hidden_layer.append(self.Neuron(input_numbers[layer_num]))
			self.layers.insert(layer_num, hidden_layer)

	def select_action(self):
		# return ID of max output
		max_output = -inf
		max_id = 0

		for output_id, output in enumerate(self.layers[self.output_layer]):
			if output > max_output:
				max_output = output
				max_id = output_id

		return max_id

	def calculate_output(self, inputs: list):
		# Calculate the first layer
		self.inputs = inputs
		next_layers_inputs = self.calculate_layer(inputs, 0)

		for layer_num in range(1, self.num_layers - 1):
			next_layers_inputs = self.calculate_layer(next_layers_inputs, layer_num)

	def calculate_layer(self, inputs: list, layer_id):
		# calculates the outputs for all the neurons in a given layer
		outputs = []

		for neuron in self.layers[layer_id]:
			neuron.inputs = inputs
			neuron.calculate_output()
			outputs.append(neuron.output)

		return outputs

	def mutate_network(self):
		# goes through entire neural network and gives each neuron a chance to mutate

		for layer in self.layers:
			for neuron in layer:
				if random() < self.mutation_chance:
					neuron.mutate_network()

	def cross_over(self, parent0, parent1):
		for layer_id, layer in enumerate(self.layers):
			for neuron_id, neuron in enumerate(layer):
				neuron = choice([parent0.layer[layer_id][neuron_id], parent1.layer[layer_id][neuron_id]])

	class Neuron:
		def __init__(self, num_inputs, bias=None, inputs=[], weights=[]):

			self.num_inputs = num_inputs
			self.num_weights = num_inputs
			self.inputs = inputs
			self.output = 0
			self.mutation_step = 0.03

			# If empty assign random weights and biases
			if bias is None:
				bias = random()

			self.bias = bias

			if len(weights) == 0:
				weights = [random() for _ in range(self.num_weights)]

			self.weights = weights

		def __eq__(self, other):
			equal = other.num_inputs == self.num_inputs
			equal = equal & (other.inputs == self.inputs)
			equal = equal & (other.bias == self.bias)
			equal = equal & (other.output == self.output)
			equal = equal & (other.weights == self.weights)
			equal = equal & (other.num_weights == self.num_weights)
			equal = equal & (other.mutation_step == self.mutation_step)
			return equal

		def __str__(self):
			return f"Inputs:{self.inputs}--Weights:{self.weights}--Bias:{self.bias}--Output:{self.output}"

		def mutate(self):
			# Adjust Bias
			self.bias += choice([-self.mutation_step, self.mutation_step])

			# Adjust Weights
			for i in range(self.num_weights):
				self.weights[i] += choice([-self.mutation_step, self.mutation_step])

		@staticmethod
		def activation(num):
			return (tanh(num) + 1) / 2

		def calculate_output(self):
			product = 0
			for i, input_value in enumerate(self.inputs):
				product += input_value * self.weights[i]

			product += self.bias

			self.output = self.activation(product)

			return self.output
