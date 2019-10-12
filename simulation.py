import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, population_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num, initial_infected=1):
        self.time_step_counter = 0
        self.pop_size = pop_size
        self.basic_repro_num = basic_repro_num
        self.population = []
        self.total_infected = 0
        self.current_infected = []
        self.newly_infected = []
        self.next_person_id = 0
        self.vacc_percentage = vacc_percentage
        self.virus_name = virus_name
        self.mortality_rate = mortality_rate
        self.file_name = f'{virus_name}_simulation_pop_{pop_size}_vp_{vacc_percentage}_infected_{initial_infected}.txt'

        self.logger = Logger(self.file_name)

        self.newly_infected = []

        self.population = self._create_population(initial_infected)

    def _create_population(self, initial_infected):
        self.population = []
        infected_count = 0
        while len(self.population) != self.pop_size:
            if infected_count != initial_infected:
                infected_person = Person(self.next_person_id, True, self.virus_name)
                self.current_infected.append(infected_person)
                self.population.append(infected_person)
                infected_count += 1
                self.next_person_id += 1
            else:
                random_created = random.random()
                if random_created < self.vacc_percentage:
                    vaccinated_person = Person(self.next_person_id, True, None)
                    self.population.append(vaccinated_person)
                    self.next_person_id += 1
                else:
                    non_vaccinated = Person(self.next_person_id, False, None)
                    self.population.append(non_vaccinated)
                    self.next_person_id += 1
        self.total_infected = infected_count
        return self.population
                    

    def _simulation_should_continue(self):
        print('total infected', self.total_infected)
        print('current infected', self.current_infected)
        print('population size', self.pop_size)
        if self.total_infected == self.pop_size:
            print('Good luck lol')
            return False
        if self.current_infected == 0:
            print('Disease too weak')
            return False
        print('Check')
        return True

    def run(self):
        Logger.write_metadata(self, self.pop_size, self.vacc_percentage, self.virus_name, self.mortality_rate, self.basic_repro_num)
        should_continue = self._simulation_should_continue()
        print(should_continue)
        self.time_step_counter = 0
        while should_continue:
            self.time_step()
            self.logger.log_time_step(self.time_step_counter)
            self.time_step_counter += 1
            should_continue = self._simulation_should_continue()
        print('The simulation has ended after {} turns.'.format(self.time_step_counter))
    

    def time_step(self):
        for person in self.population:
            for infected_person in self.current_infected:
                interactions = 0
                while interactions <= 100:
                    alive = False
                    while not alive:
                        random_person = self.population[random.randint(0, self.pop_size - 1)]
                        if random_person.is_alive:
                            alive = True
                    self.interaction(infected_person, random_person)
                    interactions += 1
        for person in self.population:
            if person.is_alive and person.infection == True:
                self.logger.log_infection_survival(person, person.did_survive_infection(self.mortality_rate))
        self.time_step_counter += 1

    def interaction(self, person, random_person):
        if random_person.is_vaccinated or random_person.infection == False:
            self.logger.log_interaction(person, random_person, False, True, False)
            return
        if random_person.is_vaccinated == False and random_person.infection == None:
            random_num = random.random()
            if random_num < self.basic_repro_num:
                self.newly_infected.append(random_person)
                self.logger.log_interaction(person, random_person)

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        for person in self.newly_infected:
            for person.id in self.population:
                person.infected = True
        self.newly_infected = []


if __name__ == "__main__":
    params = sys.argv[1:]
    name = str(params[2])
    basic_repro_rate = float(params[4])
    mortality_rate = float(params[3])
    pop_size = int(params[0])
    vacc_percentage = float(params[1])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    # virus = Virus(name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, basic_repro_rate, mortality_rate, initial_infected)

    sim.run()