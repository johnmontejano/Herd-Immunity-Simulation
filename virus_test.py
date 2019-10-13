from virus import Virus


def test_virus_instantiation():
    virus = Virus("HIV", 0.8, 0.3)
    assert virus.name == "HIV"
    assert virus.repro_rate == 0.8
    assert virus.mortality_rate == 0.3
    
    virus2 = Virus('Ebola', 0.4, 0.3)
    assert virus2.name == 'Ebola'
    assert virus2.repro_rate == 0.4
    assert virus2.mortality_rate == 0.3

