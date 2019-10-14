from person import Person
from simulation import Simulation
from logger import Logger
from virus import Virus
import pytest
import io
import sys

def test_simulation_instance():
    virus = Virus('Laughing Virus', .35, .25)
    simulation = Simulation(1000, 0.1, virus, 10)
    assert simulation.pop_size == 1000
    assert simulation.virus == virus
    assert simulation.total_infected == 10
    assert simulation.pop_size == 1000
    assert simulation.initial_infected == 10
    assert simulation.current_infected == 10
    assert simulation.newly_infected == []
    assert simulation.newly_dead == []