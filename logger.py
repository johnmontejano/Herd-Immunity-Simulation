import os
import sys
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
    # def log_interaction(self, person, random_person, random_person_sick=None,
    #                     random_person_vacc=None, did_infect=None):
    #     with open(self.file_name, 'a') as f:

    #         if random_person_sick == True and did_infect == True:
    #             f.write(f"{person._id} didn't infect {random_person._id} already sick \n")
                
    #         elif random_person_vacc == True and did_infect == True:
    #             f.write(f"{person._id} didn't infect {random_person._id} already vaccinated \n")

    #         elif did_infect == False:
    #             f.write(f"{person._id} didn't infect {random_person._id} \n")

    #         elif did_infect == True:
    #             f.write(f"{person._id} infects {random_person._id} \n")

    #         else:
    #             f.write("SHOULDN'T HAPPEN")
    def log_interaction(self, person1, person2, did_infect=None, person2_vacc=None, person2_sick=None):
        with open(self.file_name, mode='a') as f:
            f.write('Interaction Logs: \n')
            if did_infect:
                infection_status = str(person1._id) + ' infects ' + str(person2._id) + '\n'
                f.write(infection_status)
            elif person2.is_vaccinated:
                infection_status = str(person1._id) + ' did not infected ' + str(person2._id) + '\n'
                f.write(infection_status)
            else:
                infection_status = str(person1._id) + ' did not infect ' + str(person2._id) + ' because ' + str(person2._id) + ' is vaccinated or already sick.' + '\n'
                # print('Infection Status --> ', infection_status)
                f.write(infection_status)
    def log_infection_survival(self, person, did_die_from_infection):
<<<<<<< HEAD
        with open(self.file_name, mode='a') as f:
            f.write('Infection Survival: \n')
            if not did_die_from_infection:
                f.write(str(person._id) + ' survived infection' + '\n')
            else:
                f.write(str(person._id) + ' died from infection.')
=======
<<<<<<< HEAD
        ''' The Simulation object uses this method to log the results of every
        call of a Person object's .resolve_infection() method.
        The format of the log should be:
            "{person.ID} died from infection\n" or "{person.ID} survived infection.\n"
        '''
        
        with open(self.file_name, 'a') as f:
            if did_die_from_infection:
                f.write(f"{person._id} died because of infection\n")
            else:
                f.write(f"{person._id} survived the infection\n")
=======
        
>>>>>>> 209281f74393786882a23e541eccaf5fc8bbb4d8

>>>>>>> 434145310c8f4364a8477efe238c71844dd4e9cd
    def log_time_step(self, time_step_number):
        with open(self.file_name, mode='a') as f:
            f.write('Time Steps: ')
            time_step_state = str(time_step_number) + ' ended -- ' + 'Begin ' + str(time_step_number + 1) + '\n'
            f.write(time_step_state)

            