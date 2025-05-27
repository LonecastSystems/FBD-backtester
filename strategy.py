from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    max_stake: float

    def __init__(self, max_stake: float):
        self.max_stake = max_stake
        pass

    @abstractmethod
    def try_bet(self, match: pd.Series, previous_matches: pd.DataFrame) -> float:
        return 0
    
    def calculate_kelly_criterion(self, odd: float, probability: float) -> float:
        b = odd - 1
        if b == 0:
            return self.max_stake
        
        p = probability / 100
        q = 1 - p

        kc = ((b * p) - q) / b

        willing_to_risk = (self.max_stake * kc)

        return round(willing_to_risk*100) / 100