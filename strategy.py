from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    max_stake: float
    min_profit: float
    min_odds: float
    min_probability: float

    def __init__(self, max_stake: float, min_profit: float = 0.0, min_odds = 0.0, min_probability = 0.0):
        self.max_stake = max_stake
        self.min_profit = min_profit
        self.min_odds = min_odds
        self.min_probability = min_probability
        pass

    @abstractmethod
    def try_bet(self, match: pd.Series, previous_matches: pd.DataFrame) -> float:
        return 0.0
    
    def get_value_kc_bet(self, odd: float, probability: float) -> float:
        bet = 0.0
        
        if odd >= self.min_odds and probability >= self.min_probability:
            multiplier = self.calculate_value(odd, probability) / 100
            bet = self.calculate_kelly_criterion(odd, probability, multiplier)

        return bet
    
    def get_return(self, condition: bool, odd: float, probability: float) -> float:
        bet = self.get_value_kc_bet(odd, probability)

        potential = odd * bet
        profit = potential - bet
        if profit < self.min_profit:
            return 0.0

        return potential if condition else -bet

    def calculate_kelly_criterion(self, odd: float, probability: float, multiplier: float = 1.0) -> float:
        b = odd - 1
        if b == 0:
            return self.max_stake
        
        p = probability / 100
        q = 1 - p

        kc = ((b * p) - q) / b

        willing_to_risk = (self.max_stake * kc) * multiplier

        return round(willing_to_risk*100) / 100
    
    def calculate_value(self, market_odd: float, probability: float):
        if probability == 0:
            return 0
        
        odd = 1 / (probability / 100)

        if odd < market_odd:
            value = ((market_odd / odd) - 1) * 100

            return value

        return 0