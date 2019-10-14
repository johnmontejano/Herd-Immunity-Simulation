import random, sys
random.seed(42)
from person import Person
from logger import Logger
from virus import Virus


class Simulation(object):
    def __init__(self, pop_size, v_percentage, v, initial_infected=1):
        self.next_person_id = 0 # Int
        self.virus = v # Virus object
        self.pop_size = pop_size # Int
        self.initial_infected = initial_infected # Int
        self.total_infected = initial_infected# Int
        self.current_infected = initial_infected # Int
        self.vacc_percentage = v_percentage # float between 0 and 1
        self.total_dead = 0 # Int
        self.file_name = f"{self.virus.name}_simulation_pop_{self.pop_size}_vp_{self.vacc_percentage}_infected_{self.initial_infected}.txt"
        self.newly_infected = []
        self.newly_dead = []
        self.population = self._create_population(self.initial_infected)

        #Create Logger and write metadata
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(self.pop_size,self.vacc_percentage,self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

    def create_population(self, initial_infected):        
        self.population = []
        vacc_count = int(self.pop_size * self.vacc_percentage)
        for i in range(vacc_count):
            self.population.append(Person(self.next_person_id, True))
            self.next_person_id += 1
        for i in range(self.initial_infected):
            self.population.append(Person(self.next_person_id, False, self.virus))
            self.next_person_id += 1
        for person in range(self.pop_size - vacc_count - initial_infected):
            self.population.append(Person(self.next_person_id, False))
            self.next_person_id += 1
        return self.population

    def simulation_should_continue(self):
        vacc_count = 0
        self.total_dead = 0
        infected_count = 0
        for person in self.population:
            if person.is_alive and person.is_vaccinated:
                vacc_count += 1
            if person.is_alive == False:
                self.total_dead += 1
            if person.infection is not None:
                infected_count += 1
        if self.total_dead == self.pop_size or infected_count == 0:
            return False
        if vacc_count == self.pop_size - self.total_dead:
            #All survivors are vaccinated
            return False
        return True
    def run(self):
        time_step_counter = 0
        while self._simulation_should_continue():
            self.time_step()
            self.logger.log_time_step(time_step_counter)
            self._infect_newly_infected()
            time_step_counter += 1

        print(f"The simulation has ended after {time_step_counter} turns.\n")
        print(f"Population: {self.pop_size} Total Dead: {self.total_dead} Total Infected: {self.total_infected}\n")

    def time_step(self):
        for person in self.population:
            if person.is_alive and person.infection: 
                interactions = 0
                while(interactions < 100):
                    rand_person = self.population[random.randrange(0, self.pop_size)]
                    if rand_person.is_alive:
                        interactions +=1
                        self.interaction(person, rand_person)
        for person in self.population:
            if person.is_alive and person.infection:
                if person.did_survive_infection():
                    self.logger.log_infection_survival(person, False)
                else:
                    self.logger.log_infection_survival(person, True)
                    self.current_infected -= 1
                    self.total_dead += 1
                    self.newly_dead.append(person._id)



    def interaction(self, person, random_person):
        assert person.is_alive == True
        assert random_person.is_alive == True
        r_person_sick = False
        if random_person.infection is None:
            r_person_sick = False
        else:
            r_person_sick = True
        if random.random() < self.virus.repro_rate:
            self.logger.log_interaction(person, random_person, r_person_sick, random_person.is_vaccinated, True)
            if random_person.is_vaccinated is False and r_person_sick is False:
                self.newly_infected.append(random_person._id)
        else:
            self.logger.log_interaction(person, random_person, r_person_sick ,random_person.is_vaccinated, False)
    def _infect_newly_infected(self):
        for person_id in self.newly_infected:
            self.population[person_id].infection = self.virus
            self.current_infected += 1
            self.total_infected += 1
        self.newly_infected = []
        self.newly_dead = []


if __name__ == "__main__":
    params = sys.argv[1:]
    virus_name = str(params[2])
    repro_num = float(params[4])
    mortality_rate = float(params[3])

    pop_size = int(params[0])
    vacc_percentage = float(params[1])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, vacc_percentage, virus,initial_infected)

    sim.run()