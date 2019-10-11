import os
from person import Person
class Logger(object):
    def __init__(self, file_name):
        self.file_name = file_name
        f = open(self.file_name, mode='w+')
        print(f.read())
        f.close()

    def write_metadata(self, pop_size, vacc_percentage, virus_name, mortality_rate, basic_repro_num):
        with open(self.file_name, 'w') as f:
            f.write(f'{pop_size} \t {vacc_percentage} \t {virus_name} \t {mortality_rate} \t {basic_repro_num} \t \n')
        

    def log_interaction(self, person, random_person, random_person_sick=None,
                        random_person_vacc=None, did_infect=None):
        with open(self.file_name, 'a') as f:

            if random_person_sick == True and did_infect == True:
                f.write(f"{person._id} didn't infect {random_person._id} already sick \n")
                
            elif random_person_vacc == True and did_infect == True:
                f.write(f"{person._id} didn't infect {random_person._id} already vaccinated \n")

            elif did_infect == False:
                f.write(f"{person._id} didn't infect {random_person._id} \n")

            elif did_infect == True:
                f.write(f"{person._id} infects {random_person._id} \n")

            else:
                f.write("SHOULDN'T HAPPEN")


    def log_infection_survival(self, person, did_die_from_infection):
        

    def log_time_step(self, time_step_number):
        ''' STRETCH CHALLENGE DETAILS:
        If you choose to extend this method, the format of the summary statistics logged
        are up to you.
        At minimum, it should contain:
            The number of people that were infected during this specific time step.
            The number of people that died on this specific time step.
            The total number of people infected in the population, including the newly infected
            The total number of dead, including those that died during this time step.
        The format of this log should be:
            "Time step {time_step_number} ended, beginning {time_step_number + 1}\n"
        '''
        # TODO: Finish this method. This method should log when a time step ends, and a
        # new one begins.
        # NOTE: Here is an opportunity for a stretch challenge!
        pass