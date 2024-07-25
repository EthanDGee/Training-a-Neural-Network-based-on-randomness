# Goal

The goal of this program is to effectively create AIs that are good at playing the game "Bank". Ais are famously bad at
playing games that involve elements of randomness as the AIs are hard to train as worse AIs can out-compete superior
AIs. So designing ways to counteract these things are interesting. Bank also has some other interesting factors that
make it increasingly difficult to weed out good AIs from bad AIs

## Rules of Bank

To explain the rules I pulled from the most common set of rules (cited below), and rewrote some stuff to improve clarity
Bank can be played with as few as two people, but there is no upper limit to the number of people who can play. The
object of the game is to be the player with the highest score at the end of the game. Players take turns rolling two
dice and adding the value of their roll to that round’s running total. All players’ rolls contribute to the round’s
running total. The first three turns of each new round play different from the rest. Rolling a 7 is worth 70 and
everything else is just worth face value. After the third turn a 7 will end the round and reset the score to 0. To
balance this out rolling "doubles" (when the dice share face values) doubles the running point total!

At ANY time during the game a player can "Bank" to lock in the running points total add it to their score. For the rest
of the round they can't earn any more points. The remaining players continue to add to the running points total until a
7 is rolled. The players that aren't "banked" at that point don't gain any additional points.

`https://play.google.com/store/apps/details?id=com.thunderhive.bank&hl=en_US&pli=1`

# Recreating Bank

## Game Class

In charge of running the game logic and orchestrating the tournament. As well as giving players a genetic score.

### Data

- running point total
- round_num - current round number
- total_rounds - total number of rounds of play (typically ten)
- roll_num - the roll that the current round is on
- rolls_since_double - number of rolls since the last double
- STARTER_ROUNDS (3) - number of starter rounds
- player_count - number of players in given game
- remaining_players - the amount of players remaining in a given round.
- players - list of players

### Key Methods

- roll_dice - updates the score, roll information, and ends the round if a 7 is rolled outside the starter rounds.
- play_game
- print_score_card
- ask_players_about_banking
- adjust_genetic_score
- filter_players - remove unfit players from tournament

## Player Class

In charge of deciding whether to bank after a given roll. as well as genetic tomfoolery

## Data

id
score - genetic_score
game_score - score for current game
banked - whether or not a player has banked in the current round

