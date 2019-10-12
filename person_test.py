import pytest
from person import Person
from virus import Virus
import io
import sys
import random


def test_vacc_person_instantiation():
    person = Person(1, True, None)
    assert person._id == 1
    assert person.is_alive is True
    assert person.is_vaccinated is True
    assert person.infection is None


def test_not_vacc_person_instantiation():
    person = Person(2, False, None)
    assert person.is_alive is True
    assert person.is_vaccinated is False
    assert person.infection is None


def test_sick_person_instantiation():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(3, False, virus)
    assert person.is_alive is True
    assert person.is_vaccinated is False


def test_did_survive_infection():
    virus = Virus("Dysentery", 0.7, 0.2)
    person = Person(4, False, virus)

    survived = person.did_survive_infection()
    if survived:
        assert person.is_alive is True
        assert person.is_vaccinated is False
        assert person.infection is virus
    else:
        assert person.is_alive is False
        assert person.is_vaccinated is False
        assert person.infection is virus