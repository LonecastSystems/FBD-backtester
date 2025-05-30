from datetime import datetime, timedelta
from typing import List
import pandas as pd
import strategy

class Backtester:
    history = []
    bankroll: float
    strats: List[strategy.Strategy]

    def __init__(self, strats: List[strategy.Strategy], bankroll: float):
        self.strats = strats
        self.bankroll = bankroll
        pass

    def backtest(self, df: pd.DataFrame, search_days_back: int) -> float:
        days_back_from_now_str = (datetime.today() - timedelta(days=search_days_back)).strftime('%Y-%m-%d')
        recent_matches = df.loc[(df['DATE'] > days_back_from_now_str)].copy()

        if len(recent_matches.index) == 0:
            return 0
        
        profit = 0
        for i, row in recent_matches.iterrows():
            date = row['DATE']
            bt_df = df.loc[(df['DATE'] < date)].copy()
            
            num_bets = 0
            correct_bets = 0
            match_profit = 0

            for strat in self.strats:
                curr_profit = strat.try_bet(row, bt_df)
                if curr_profit == 0:
                    continue
                else:
                    num_bets += 1
                    if curr_profit > 0:
                        correct_bets += 1

                self.bankroll += curr_profit
                match_profit += curr_profit
                profit += curr_profit

            self.history.append({
                "date": date,
                "bankroll": self.bankroll,
                "num_bets": num_bets,
                "correct_bets": correct_bets,
                "match_profit": match_profit
            })

        return profit