"""
Calculates basic stats on a player
"""
def stats(player):
  games = player.completed_games()
  wins = 0
  for game in games:
    if game.winner().key() == player.key():
      wins += 1
  return {
    'losses': len(games) - wins,
    'wins': wins,
    'percent_win': int(100 * float(wins) / len(games))
  }