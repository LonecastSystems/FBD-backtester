from datetime import datetime, timedelta
import unittest
import numpy as np
import pandas as pd
from strategy import Strategy
from backtester import Backtester

class SampleStrategy(Strategy):
    def try_bet(self, match: pd.Series, previous_matches: pd.DataFrame) -> float:
        res = match['RES']

        h_column = f"BF EX H ODDS"
        h_odd = match[h_column]

        meanH = previous_matches[h_column].mean()
        res_d = (previous_matches['RES'].value_counts(normalize=True) * 100).to_dict()

        h_prob = res_d['H'] if 'H' in res_d else 0

        if h_odd < meanH:
            bet = self.calculate_kelly_criterion(h_odd, h_prob)

            return bet if res == 'H' else -bet

        return 0

class TestBacktester(unittest.TestCase):
    def test_backtest(self):
        sample = SampleStrategy(25.0)
        
        today = datetime.today()
        dates = [today - timedelta(days=i) for i in range(10)]

        # Simulate data
        data = {
            'DATE': dates,
            'RES': np.random.choice(['H', 'D', 'A'], size=10),  # H = Home Win, D = Draw, A = Away Win
            'BF EX H ODDS': np.round(np.random.uniform(1.5, 3.5, size=10), 2)  # Simulated home odds
        }

        df = pd.DataFrame(data)

        bt = Backtester([sample], df)

        profit = bt.backtest(1000, 5)

        history = bt.history

        self.assertEqual(len(history), 6)
        self.assertNotEqual(profit, 0)

        for h in history.items():
            print("\n", h)

        print(profit)

    if __name__ == '__main__':
        unittest.main()