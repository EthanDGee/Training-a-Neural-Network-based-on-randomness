from math import inf, tanh
from random import random, choice
from copy import deepcopy


class NeuralNetwork:
	def __init__(self, num_inputs, layer_layout):
		# Layer layout is formatted like [5,3,3] which means 3 hidden layers with the requisite amount of neurons
		self.num_inputs = num_inputs
		self.inputs = []

		self.num_outputs = layer_layout[-1]
		self.output_layer = len(layer_layout) - 1

		self.num_layers = len(layer_layout)
		self.layers = []

		self.mutation_chance = 0.1

		# Create Random Layers
		input_numbers = deepcopy(layer_layout)
		input_numbers.insert(0, num_inputs)

		for layer_num, neuron_amount in enumerate(layer_layout):
			hidden_layer = []

			for i in range(neuron_amount):
				new_neuron = self.Neuron(input_numbers[layer_num])
				hidden_layer.append(new_neuron)
				del new_neuron

			self.layers.insert(layer_num, hidden_layer)

	def __eq__(self, other):
		for layer_id, layer in enumerate(self.layers):
			# for neuron in range(len(layer)):
			# 	print(layer[neuron])
			# 	print(self.layers[layer_id][neuron])
			if layer != other.layers[layer_id]:
				return False
			# for neuron_id, neuron in enumerate(layer):
			# 	if neuron != other.layers[layer_id][neuron_id]:
			# 		 print(f"{neuron}{other.layers[layer_id][neuron_id]}")
			# 		return False
		return True

	def check_network_from_parents(self, parent_0, parent_1):

		for layer_id, layer in enumerate(self.layers):
			for neuron_id, neuron in enumerate(layer):
				# checks to see that neuron matches  one of the parents
				if not (neuron == parent_0.layers[layer_id][neuron_id]) or (
						neuron == parent_1.layers[layer_id][neuron_id]):
					print(f"{layer_id}, {neuron_id}")
					return False

		return True

	def select_action(self):
		# return ID of max output
		max_output = -inf
		max_id = 0

		for output_id, output_neuron in enumerate(self.layers[self.output_layer]):
			if output_neuron.output > max_output:
				max_output = output_neuron.output
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
					neuron.mutate()

	def cross_over(self, parent0, parent1):
		self.layers = parent0.layers
		self.inputs = parent0.inputs

		# print(len(self.layers))
		for layer_id, layer in enumerate(self.layers):
			for neuron_id, neuron in enumerate(layer):
				# print(f"{layer_id}, {neuron_id}")
				# print(type(parent0.layers[layer_id][neuron_id]))
				# print(type(parent1.layers[layer_id][neuron_id]))
				# Select a neuron from of the parents
				possible_neurons = [parent0.layers[layer_id][neuron_id], parent1.layers[layer_id][neuron_id]]

				self.layers[layer_id][neuron_id] = choice(possible_neurons)

				# if self.layers[layer_id][neuron_id] == parent0.layers[layer_id][neuron_id]:
				# 	print("Neuron 0 Selected")
				# else:
				# 	print("Neuron 1 Selected")

	class Neuron:
		def __init__(self, num_inputs, bias=None, inputs=[], weights=[]):

			self.num_inputs = num_inputs
			self.num_weights = num_inputs
			self.inputs = inputs
			self.output = 0
			self.mutation_step = 0.05

			# If empty assign random weights and biases
			if bias is None:
				bias = random()

			self.bias = bias

			if len(weights) == 0:
				weights = [random() for _ in range(self.num_weights)]

			self.weights = weights

		def __eq__(self, other):
			equal = self.bias == other.bias
			equal = equal & (other.weights == self.weights)
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
