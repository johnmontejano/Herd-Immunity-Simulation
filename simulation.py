import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, pop_size, vacc_percentage, mortality_rate, basic_repro_num, initial_infected=1, virus):
        # TODO: Call self._create_population() and pass in the correct parameters.
        # Store the array that this method will return in the self.population attribute.
        # TODO: Store each newly infected person's ID in newly_infected attribute.
        # At the end of each time step, call self._infect_newly_infected()
        # and then reset .newly_infected back to an empty list.
        self.logger = Logger(self.file_name)
        self.population = _create_population(initial_infected) # List of Person objects
        self.pop_size = pop_size # Int
        self.next_person_id = 0 # Int
        self.virus = virus # Virus object
        self.initial_infected = initial_infected # Int
        self.total_infected = 0 # Int
        self.current_infected = 0 # Int
        self.vacc_percentage = vacc_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = "{}_simulation_pop_{}_vp_{}_infected_{}.txt".format(virus_name, population_size, vacc_percentage, initial_infected)
        self.newly_infected = []
        self.basic_repro_num = basic_repro_num
        self.mortality_rate = mortality_rate
        self.virus_name = virus_name

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
        time_step_counter = 0
        while should_continue:
            self.time_step()
            self.logger.log_time_step(self.time_step_counter)
            self.time_step_counter += 1
            should_continue = self._simulation_should_continue()
        print('The simulation has ended after {} turns.'.format(self.time_step_counter))
    

    def time_step(self):
        ''' This method should contain all the logic for computing one time step
        in the simulation.
        This includes:
            1. 100 total interactions with a randon person for each infected person
                in the population
            2. If the person is dead, grab another random person from the population.
                Since we don't interact with dead people, this does not count as an interaction.
            3. Otherwise call simulation.interaction(person, random_person) and
                increment interaction counter by 1.
            '''
        # TODO: Finish this method.
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
        '''This method should be called any time two living people are selected for an
        interaction. It assumes that only living people are passed in as parameters.
        Args:
            person1 (person): The initial infected person
            random_person (person): The person that person1 interacts with.
        '''
        # Assert statements are included to make sure that only living people are passed
        # in as params
        assert person.is_alive == True
        assert random_person.is_alive == True

        # TODO: Finish this method.
        #  The possible cases you'll need to cover are listed below:
            # random_person is vaccinated:
            #     nothing happens to random person.
            # random_person is already infected:
            #     nothing happens to random person.
            # random_person is healthy, but unvaccinated:
            #     generate a random number between 0 and 1.  If that number is smaller
            #     than repro_rate, random_person's ID should be appended to
            #     Simulation object's newly_infected array, so that their .infected
            #     attribute can be changed to True at the end of the time step.
        # TODO: Call slogger method during this method.
        pass

    def _infect_newly_infected(self):
        ''' This method should iterate through the list of ._id stored in self.newly_infected
        and update each Person object with the disease. '''
        # TODO: Call this method at the end of every time step and infect each Person.
        # TODO: Once you have iterated through the entire list of self.newly_infected, remember
        # to reset self.newly_infected back to an empty list.
        pass


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[0])
    repro_num = float(params[1])
    mortality_rate = float(params[2])

    pop_size = int(params[3])
    vacc_percentage = float(params[4])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(name, repro_rate, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, initial_infected, virus)

    sim.run()