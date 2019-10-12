import random
random.seed(42)
from virus import Virus


class Person(object):
    def __init__(self, _id, is_vaccinated, infection=None):
        self._id = _id
        self.is_alive = True  
        self.is_vaccinated = is_vaccinated 
        self.infection = infection 
    def did_survive_infection(self):
        mortality_rate = self.infection.mortality_rate
        if self.infection:
            random_float = random.random()
            if random_float > mortality_rate:
                self.is_vaccinated = True
                self.infected = None
                return True
            else:
                self.is_alive = False
                return False