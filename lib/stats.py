"""
Calculates basic stats on a player
"""
def stats(player):
  games = player.completed_games()
  wins = 0
  losses = 0
  for game in games:
    if game.winner().key() == player.key():
      wins += 1
    else:
      losses += 1
  return { 'losses' : losses, 'wins' : wins }