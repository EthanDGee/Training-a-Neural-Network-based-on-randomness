# KEY CHALLENGES

- Bank is inherently random so bad AIs can out-compete good AIs and cause training issues
- Adjusting for the challenge of increased player count increase randomness and chance for training issues

MY idea for training is that I set it up the player as neural network with the following parameters that go into the
decision as to whether or not to bank on a given round, with the goal of simulating a human as much as possible without
adding inputs that might confuse the neural network/add unnecessary complexity.

## Inputs

- running_point_total []
- roll_num
- rolls_since_double
- percent_remaining_players
- game_score
- percent_of_rounds_completed
- percent_difference_between_top_players

Inputs that I chose not to implement

- roll_num_difference_from_average_seven
- rolls_similarity_seven
- times_banked

# Scoring the Players Performance

As the score is ultimately only part of how good a person is at the game, lets build this formula in parts

## PROs and CONs of different Metrics

## Simple Score

- Pros: it's what the goal of the game is
- cons: Spread across the entire tournament the early rounds would have significantly more weight than the later rounds
  as more people = higher possible score, and this score is much more susceptible to chance dominating the results

## Comparing score to perfect game

- Pros: its an easy metric to implement
- Cons: It would lead to players being rewarded based on how close they got to the last roll over all else, meaning
  risky plays are the ones that get the most benefit

## Simple Rank

- Pros: It's what ultimately matters, and can be compared easily across different group sizes
- Cons: It's a little harder for a good AI to Maintain rank

## Design

After each Game Players will be sorted by game score and then assigned a score based on percentage position * an
arbitrary positive number so that people at the top are generally rewarded at similar levels (in order to avoid a random
run of good luck from affecting the ranking), as well as, so that they can easily by compared across tournament levels.
As placing in the top XX% will give always give you 1-XX% of the points.

Equation

```
self.players sorted(bank.players, key=lambda y: y.game_score) # these are sorted in ascending order
for placement, player in iter(self.players):
	player.score += placement/self.player_count * 100

```

# Orchestrating competition

The other half of mitigating the effects randomness is in the selection/training process Bank is a game of chance that
is heavily affected by player number so it's incredibly important for it to be able to train it with varied amount of
players. Knowing this I've decided to structure out the training process in the form of a tournament.

## Tournament structuring

Players will start out in game of 50 players made up of past players, and genetic descendants will play a series of
games followed by them being sorted by there genetic score, the bottom ten will then be removed from the game and they
will play a few more games until they reach 10 players where they will play one more series of games after which the top
5 will be selected for reproduction where they will then have 3 sets of kids with every combo (5 choose 2 is 10 so we're
shooting for 30 replacements) the kids will be mutated and proceed to play a new series of games. With the rest of the
top ten thrown in to compete as well , in addition to the 5 players from 3 and 5 rounds ago as a further assurance to 
prevent bad actors from affecting the gene pool

In general a round of play will last around 6 dice rolls (not including starter rolls) knowing this and that the
chances of a getting to 12 are only around 11.22%, so regularly betting on getting to 12 isn't the smartest and not a
great long term strategy, however it does lead to some really high numbers that could upend training. This of course
doesn't consider factors a human would but it is acceptable for a risky bet. In order for them to reach the top 50% to 
reproduce they need to hit there bet consistently more often for each tournament level. 1/5 of the time for the first
level, 1/4 for the second, and so on until they need to hit 1/2 of the time for the final level. Calculating the odds
for them to reach the top 5 overall after five games we can be comfortable confident that they will be removed from
the gene pool

## Strategies for mitigating randomness

- Playing multiple rounds
- tournament style to slowly select best player meaning bad actors need to consistently out plays 
- Using elders (5 rounds ago 3) as a means to compare new strategies with old strategies. 