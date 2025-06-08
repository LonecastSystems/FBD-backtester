from abc import ABC, abstractmethod
from typing import List
import pandas as pd

class Strategy(ABC):
    max_stake: float
    min_profit: float
    min_odds: float
    min_probability: float
    min_value: float

    def __init__(self, max_stake: float, min_profit: float = 0.0, min_odds: float = 0.0, min_probability: float = 0.0, min_value: float = 0.0):
        self.max_stake = max_stake
        self.min_profit = min_profit
        self.min_odds = min_odds
        self.min_probability = min_probability
        self.min_value = min_value
        pass

    @abstractmethod
    def try_bet(self, match: pd.Series, previous_matches: pd.DataFrame) -> List[float]:
        return [0.0]
    
    def calculate_value(self, market_odd: float, probability: float) -> tuple[float, float]:
        if probability == 0:
            return 0.0, 0.0
        
        prob_short = probability / 100
        roi = ((market_odd * prob_short) - 1) * 100
        exp = (((self.max_stake * market_odd) - self.max_stake) * prob_short) - (self.max_stake * (1 - prob_short))

        if exp < self.min_value:
            return 0.0, 0.0

        return round(roi, 2), round(exp, 2)

    def calculate_kelly_criterion(self, odd: float, probability: float, multiplier: float = 1.0) -> float:
        if odd < self.min_odds or probability < self.min_probability:
            return 0.0

        b = odd - 1
        if b == 0:
            return self.max_stake
        
        p = probability / 100
        q = 1 - p

        kc = ((b * p) - q) / b

        willing_to_risk = (self.max_stake * kc) * multiplier

        return round(willing_to_risk, 2)
    
    def calculate_return(self, condition: bool, odd: float, bet: float) -> float:
        potential = odd * bet
        profit = potential - bet
        if profit < self.min_profit:
            return 0.0

        return potential if condition else -bet