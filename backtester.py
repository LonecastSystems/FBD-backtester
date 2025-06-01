from datetime import datetime, timedelta
from typing import List
import pandas as pd
import strategy

class Backtester:
    strats: List[strategy.Strategy]

    def __init__(self, strats: List[strategy.Strategy]):
        self.strats = strats
        pass

    def backtest(self, df: pd.DataFrame, bankroll: float, start_date: datetime, end_date: datetime = datetime.today()):
        lower_bound = start_date.strftime('%Y-%m-%d')
        upper_bound = end_date.strftime('%Y-%m-%d')
        recent_matches = df.loc[(df['DATE'] > lower_bound) & (df['DATE'] <= upper_bound)].copy()

        history = []
        result = {
            "bankroll": bankroll, 
            "profit": 0.0,
            "num_bets": 0,
            "correct_bets": 0
        }
        
        for i, row in recent_matches.iterrows():
            date = row['DATE']
            bt_df = df.loc[(df['DATE'] < date)].copy()
            
            match_profit = 0
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
                match_profit += curr_profit

            history.append({
                "date": date,
                "bankroll": bankroll,
                "profit": match_profit,
                "num_bets": num_bets,
                "correct_bets": correct_bets
            })

            result["bankroll"] += match_profit
            result["profit"] += match_profit
            result["num_bets"] += num_bets
            result["correct_bets"] += correct_bets

        return result, history