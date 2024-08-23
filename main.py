from Game import Game

if __name__ == '__main__':
	bank = Game(10, 10)
	if input("Input Players? (y/n) ").lower() == 'y':
		bank.import_players(input("Enter file_name: "))
		bank.generate_new_tournament_players()

	save_file = input("Enter save file name: ")

	bank.train(50, save_file)
	# bank.run_tournament()
	print("RESULTS")

	bank.print_score_card()
