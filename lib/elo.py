"""
A super basic implementation of the ELO ranking algorithm. The advantage
of this algorithm is that it's very simple and does not require any more information
than an individual match in order to update rankings.

The downside is that ELO doesn't take into account the actual score, just a win/lose.

It updates rankings step-wise, and is expected to be called for each game in succession.

http://en.wikipedia.org/wiki/Elo_rating_system

Especially: see http://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details
"""
MAX_INCREASE = 32
INITIAL_RANK = 1500.0

def update_ranks(game):
  player_1 = game.player_1
  player_2 = game.player_2

  expected_1 = expected(player_2.rank, player_1.rank)
  expected_2 = expected(player_1.rank, player_2.rank)

  if game.winner == game.player_1:
    score_1 = 1
    score_2 = 0
  else:
    score_1 = 0
    score_2 = 1

  update_player_rank(player_1, score_1, expected_1)
  update_player_rank(player_2, score_2, expected_2)

def expected(rank_1, rank_2):
  return 1 / (1 + 10 ** (float(rank_1 - rank_2) / 400))

def update_player_rank(player, score, expected):
  player.rank += (MAX_INCREASE * (score - expected))

def max_increase(rank):
  """
  Determines the maximum possible points that a player can get in any given match
  see http://en.wikipedia.org/wiki/Elo_rating_system#Most_accurate_K-factor
  """
  if rank <= 2100:
    return 32
  if 2100 < rank <= 2400:
    return 24
  if 2400 < rank:
    return 16

