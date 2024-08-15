from Game import Game

if __name__ == '__main__':
	bank = Game(10, 10)
	for _ in range(5):
		bank.run_tournament()
		bank.generate_new_tournament_players()
		bank.print_score_card()
