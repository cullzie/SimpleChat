import unittest
import datetime as dt
from dtos.User import User


class TestUser(unittest.TestCase):
    def test_create_blank_user(self):
        user = User()
        self.assertIsNone(user.name, None)
        self.assertIsNone(user.date_of_birth, None)
        self.assertIsNone(user.gender, None)
        self.assertIsNone(user.smoker, None)

    def test_set_name(self):
        name = 'Frank'
        user = User()

        user.name = name
        self.assertEqual(user._name, name)  # Checks private var has been set

    def test_get_name(self):
        name = 'Mary'
        user = User()

        user.name = name
        self.assertEqual(user.name, name)  # Checks getter is set

    def test_set_valid_date_of_birth(self):
        dob = '07-02-1976'
        user = User()

        user.date_of_birth = dob
        expected_date_of_birth = dt.datetime.strptime(dob, '%d-%m-%Y').isoformat()
        self.assertEqual(user._date_of_birth, expected_date_of_birth)  # Checks private var has been set

    def test_set_date_of_birth_invalid(self):
        user = User()
        with self.assertRaises(ValueError):
            user.date_of_birth = '10-09/1990'

    def test_get_date_of_birth(self):
        dob = '22-03-1955'
        user = User()

        user.date_of_birth = dob
        expected_date_of_birth = dt.datetime.strptime(dob, '%d-%m-%Y').isoformat()
        self.assertEqual(user.date_of_birth, expected_date_of_birth)  # Checks getter is set

    def test_set_gender_female(self):
        gender = 'Female'
        user = User()

        user.gender = gender
        self.assertEqual(user._gender, gender)  # Checks private var has been set

    def test_set_gender_male(self):
        gender = 'Male'
        user = User()

        user.gender = gender
        self.assertEqual(user._gender, gender)  # Checks private var has been set

    def test_set_gender_invalid(self):
        gender = 'Something else'
        user = User()

        with self.assertRaises(TypeError):
            user.gender = gender

    def test_get_gender(self):
        gender = 'Male'
        user = User()

        user.gender = gender
        self.assertEqual(user.gender, gender)  # Checks getter is set

    def test_set_smoker_yes(self):
        smoker = 'Yes'
        user = User()

        user.smoker = smoker
        self.assertTrue(user._is_smoker)  # Checks private var has been set

    def test_set_smoker_no(self):
        smoker = 'No'
        user = User()

        user.smoker = smoker
        self.assertFalse(user._is_smoker)  # Checks private var has been set

    def test_set_smoker_invalid(self):
        smoker = 'I have not smoked'
        user = User()

        with self.assertRaises(TypeError):
            user.smoker = smoker

    def test_get_smoker(self):
        smoker = 'No'
        user = User()

        user.smoker = smoker
        self.assertFalse(user.smoker)  # Checks getter is set

    def test_string_representation_of_user(self):
        user = User()
        user.name = 'Patrick'
        user.date_of_birth = '10-10-1988'
        user.gender = 'Male'
        user.smoker = 'No'

        self.assertEqual(str(user), 'Patrick was born on 10-10-1988 and is a Male non-smoker')

    def test_string_representation_of_user_invalid(self):
        user = User()
        user.name = 'Ann'
        user.gender = 'Female'
        user.smoker = 'Yes'

        self.assertEqual(str(user), '')  # Return empty string repr if we are missing some parameters


if __name__ == 'main':
    unittest.main()
