import random, sys
from person import Person
from logger import Logger
from virus import Virus
random.seed(42)

#code that runs the sim. Includes the population size, vaccination percentage, the virus, and the initially infecteed
class Simulation(object):
    def __init__(self, pop_size, v_percentage, v, initial_infected=1):
        self.pop_size = pop_size
        self.v_percentage = v_percentage
        self.virus = v
        self.initial_infected = initial_infected
        self.total_infected = initial_infected
        self.current_infected = initial_infected
        self.newly_infected = []
        self.next_person_id = 0
        self.total_dead = 0 # Int
        self.file_name = f"{self.virus.name}_simulation_pop_{self.pop_size}_vp_{self.v_percentage}_infected_{self.initial_infected}.txt"
        self.newly_dead = []
        self.population = self.create_population(self.initial_infected)
        self.logger = Logger(self.file_name)
        self.logger.write_metadata(self.pop_size,self.v_percentage,self.virus.name, self.virus.mortality_rate, self.virus.repro_rate)

    #code that creates the population including the initially infected
    def create_population(self, initial_infected):        
        self.population = []
        v_count = int(self.pop_size * self.v_percentage)
        for i in range(v_count):
            self.population.append(Person(self.next_person_id, True))
            self.next_person_id += 1
        for i in range(self.initial_infected):
            self.population.append(Person(self.next_person_id, False, self.virus))
            self.next_person_id += 1
        for person in range(self.pop_size - v_count - initial_infected):
            self.population.append(Person(self.next_person_id, False))
            self.next_person_id += 1
        return self.population

    #decides wether simulation should continue or not
    #sim will end if everyone is dead and/or nobody is infected
    def simulation_should_continue(self):
        v_count = 0
        self.total_dead = 0
        infected_count = 0
        for person in self.population:
            if person.is_alive and person.is_vaccinated:
                v_count += 1
            if person.is_alive == False:
                self.total_dead += 1
            if person.infection is not None:
                infected_count += 1
        if self.total_dead == self.pop_size or infected_count == 0:
            return False
        if v_count == self.pop_size - self.total_dead:
            #All survivors are vaccinated
            return False
        return True
    
    #runs the sim while simulation_should_continue() method is True
    def run(self):
        time_step_counter = 0
        while self.simulation_should_continue():
            self.time_step()
            self.logger.log_time_step(time_step_counter)
            self._infect_newly_infected()
            time_step_counter += 1
        print(f"Simulation has ended after {time_step_counter} turns.\n")
        print(f"Population size: {self.pop_size} Total Dead: {self.total_dead} Total Infected: {self.total_infected}\n")
    
   #makes every infected person interact with 100 people that are not infected 
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
    
    #
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
    v_percentage = float(params[1])

    if len(params) == 6:
        initial_infected = int(params[5])
    else:
        initial_infected = 1

    virus = Virus(virus_name, repro_num, mortality_rate)
    sim = Simulation(pop_size, v_percentage, virus,initial_infected)

    sim.run()