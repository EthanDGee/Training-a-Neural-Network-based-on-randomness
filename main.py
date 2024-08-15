from Game import Game

if __name__ == '__main__':
	bank = Game(10, 10)
	if input("Input Players? (y/n) ").lower() == 'y':
		bank.import_players()

	save_file = input("Enter save file name: ")

	bank.train(10, save_file)
