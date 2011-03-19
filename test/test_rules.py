import unittest

import sys
sys.path.append("../lib")
import rules

class TestRules(unittest.TestCase):

    def setUp(self):
      pass

    def test_validate_non_negative(self):
        # should raise an exception for a negative score
        self.assertRaises(Exception, rules.validate_non_negative, -1)

    def test_validate_min_score(self):
      # should raise an exception if no one made it to 21 points
      self.assertRaises(Exception, rules.validate_min_score, 20, 20)

    def test_validate_score_diff(self):
      # should raise an exception if the score is above 21 and doesn't have a difference of 2
      self.assertRaises(Exception, rules.validate_score_diff, 21, 22)
      self.assertRaises(Exception, rules.validate_score_diff, 20, 21)

      # should pass validation
      rules.validate_score_diff(21, 0)
      rules.validate_score_diff(21, 19)

    def test_validate_not_huge(self):
      # should raise an exception if the score is way high
      self.assertRaises(Exception, rules.validate_not_huge, 1000)

if __name__ == '__main__':
    unittest.main()

