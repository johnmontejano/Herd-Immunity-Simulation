class Virus(object):
    def __init__(self, name, mortality_rate, repro_rate):
        self.name = name
        self.mortality_rate = mortality_rate
        self.repro_rate = repro_rate


def test_virus_instantiation():
    #TODO: Create your own test that models the virus you are working with
    '''Check to make sure that the virus instantiator is working.'''
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3
    
    virus2 = Virus('Ebola', 0.4, 0.3)
    assert virus2.name == 'Ebola'
    assert virus2.repro_rate == 0.4
    assert virus2.mortality_rate == 0.3

