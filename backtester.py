from datetime import datetime, timedelta
from typing import List
import pandas as pd
import strategy

class Backtester:
    history = {}

    strats: List[strategy.Strategy]
    df: pd.DataFrame

    def __init__(self, strats: List[strategy.Strategy], df: pd.DataFrame):
        self.strats = strats
        self.df = df
        pass

    def backtest(self, bankroll: float, search_days_back: int) -> float:
        self.history = {}

        days_back_from_now_str =  (datetime.today() - timedelta(days=search_days_back)).strftime('%Y-%m-%d')
        recent_matches = self.df.loc[(self.df['DATE'] > days_back_from_now_str)].copy()

        if len(recent_matches.index) == 0:
            return 0
        
        profit = 0
        for i, row in recent_matches.iterrows():
            date = row['DATE']
            bt_df = self.df.loc[(self.df['DATE'] < date)].copy()
            
            num_bets = 0
            correct_bets = 0

            for strat in self.strats:
                curr_profit = strat.try_bet(row, bt_df)
                if curr_profit == 0:
                    continue
                else:
                    num_bets += 1
                    if curr_profit > 0:
                        correct_bets += 1

                bankroll += curr_profit
                profit += curr_profit

            self.history[i] = {
                "date": date,
                "bankroll": bankroll,
                "num_bets": num_bets,
                "correct_bets": correct_bets,
            }

        return profit