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

def test_create_population():
    virus = Virus('Laughing Virus', .35, .25)
    simulation = Simulation(1000, 0.1, virus, 10)
    vacc_count = 0
    infected_count = 0
    for person in simulation.population:
        assert person.is_alive == True
        if person.is_vaccinated:
            vacc_count += 1
        if person.infection != None:
            infected_count +=1
    assert vacc_count == 100
    assert infected_count == 10
    assert len(simulation.population) == 1000

def test_simulation_should_continue():
    virus = Virus('Laughing Virus', .35, .25)
    simulation = Simulation(1000, 0.1, virus, 10)
    for person in simulation.population:
        person.is_alive == False
    assert simulation.simulation_should_continue() == True
