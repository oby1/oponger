"""
Calculates basic stats on a player
"""
def stats(player):
  games = player.completed_games()
  wins = 0
  for game in games:
    if game.winner.key() == player.key():
      wins += 1

  num_games = len(games)
  percent_win = 0 if num_games == 0 else int(100 * float(wins) / len(games))
  return {
    'losses': len(games) - wins,
    'wins': wins,
    'percent_win': percent_win
  }