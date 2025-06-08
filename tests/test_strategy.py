from typing import List
import unittest
from strategy import Strategy
import pandas as pd

class SampleStrategy(Strategy):
    def try_bet(self, match: pd.Series, previous_matches: pd.DataFrame) -> List[float]:
        return [0]

class TestStrategy(unittest.TestCase):
    def test_calculate_kelly_criterion(self):
        sample = SampleStrategy(25.0)
        bet = sample.calculate_kelly_criterion(1.6, 70)
        
        self.assertEqual(bet, 5.0)

        bet = sample.calculate_kelly_criterion(1.9, 78)
        
        self.assertEqual(bet, 13.39)

    def test_calculate_value(self):
        sample = SampleStrategy(25.0)
        roi, value = sample.calculate_value(2.3, 50)
        
        self.assertEqual(roi, 15.00)
        self.assertEqual(value, 3.75)