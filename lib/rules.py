"""
A central place for the ping pong rules.
"""
import math

POINTS_TO_WIN = 21
POINT_DIFF_FOR_WIN = 2 # if the game goes above 21
MAX_REASONABLE_SCORE = 100 # should be crazy rare to get this sort of score

def validate_scores(player_1_score, player_2_score):
  validate_non_negative(player_1_score)
  validate_non_negative(player_2_score)
  validate_min_score(player_1_score, player_2_score)
  validate_score_diff(player_1_score, player_2_score)
  validate_not_huge(player_1_score)
  validate_not_huge(player_2_score)

def validate_non_negative(player_score):
  if player_score < 0:
    raise Exception("Can't have a negative score, but got %s" % player_score)

def validate_min_score(player_1_score, player_2_score):
  if player_1_score < POINTS_TO_WIN and player_2_score < POINTS_TO_WIN:
    raise Exception("""Can't have a winner without someone making it to %s points,
but got %s and %s points for players.""" % (POINTS_TO_WIN, player_1_score, player_2_score))

def validate_score_diff(player_1_score, player_2_score):
  if (player_1_score > POINTS_TO_WIN - 1 or player_2_score > POINTS_TO_WIN - 1)\
      and math.fabs(player_1_score - player_2_score) < POINT_DIFF_FOR_WIN:
    raise Exception("Invalid win difference, got %s and %s points for players."
    % (player_1_score, player_2_score))

def validate_not_huge(player_score):
  if player_score > MAX_REASONABLE_SCORE:
    raise Exception("Score %s is way huge and we allow a maximum of %s" % (player_score, MAX_REASONABLE_SCORE))

