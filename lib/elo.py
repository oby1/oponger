"""
A super basic implementation of the ELO ranking algorithm. The advantage
of this algorithm is that it's very simple and does not require any more information
than an individual match in order to update rankings.

The downside is that ELO doesn't take into account the actual score, just a win/lose.

It updates rankings step-wise, and is expected to be called for each game in succession.

http://en.wikipedia.org/wiki/Elo_rating_system
"""
MAX_INCREASE = 32
INITIAL_RANK = 1500

def update_scores(game):
  e1 = expected(game.player_2_score, game.player_1_score)
  e2 = expected(game.player_1_score, game.player_2_score)
  if game.player_1_score > game.player_2_score:
    game.player_1.rank += e2
    game.player_2.rank -= e2
  else:
    game.player_1.rank -= e1
    game.player_2.rank += e1

def expected(score_1, score_2):
  return MAX_INCREASE * 1 / (1 + 10 ** ((score_1 - score_2) / 400))

