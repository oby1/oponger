import unittest

import sys
sys.path.append("../lib")
import elo

class TestRules(unittest.TestCase):
  """
  Test that the ELO algorithm works, but only check that the integer rounding values are close.
  I.e. check for "good enough"
  """

  def setUp(self):
      pass

  def test_rank_using_wikipedia_example(self):
    player = mock_player(1613)
    elo.update_ranks(game(player, mock_player(1609), False))
    elo.update_ranks(game(player, mock_player(1388), True))
    elo.update_ranks(game(player, mock_player(1586), True))
    elo.update_ranks(game(player, mock_player(1720), False))
    # 1613 + 32 * (2 - 2.181), almost
    self.assertAlmostEquals(1608, player.rank, 0)

  def test_example_1(self):
    # example 1 from http://www.chesselo.com/, except using K=32
    player = mock_player(2000)
    elo.update_ranks(game(player, mock_player(1900), True))
    # 2000 + 32 * (1 - 0.64)
    self.assertAlmostEquals(2012, player.rank, 0)

  def test_example_2(self):
    # example 2 from http://www.chesselo.com/, except using K=32
    player = mock_player(2000)
    elo.update_ranks(game(player, mock_player(1900), False))
    # 2000 + 32 * (0 - 0.64)
    self.assertAlmostEquals(1980, player.rank, 0)


class mock_player():
  def __init__(self, rank):
    self.rank = rank

class game():
  def __init__(self, player_1, player_2, player_1_win):
    self.player_1 = player_1
    self.player_2 = player_2
    self.player_1_score = 21 if player_1_win else 19
    self.player_2_score = 19 if player_1_win else 21

if __name__ == '__main__':
    unittest.main()

