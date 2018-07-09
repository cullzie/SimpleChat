import datetime as dt
import logging
from dateutil import parser

logger = logging.getLogger(__name__)


class User(object):
    """
    This is a simple representation of the user within our application
    Can be expanded and used to persist data to the DB when the time comes
    """

    def __init__(self, name=None, date_of_birth=None, smoker=None, gender=None):
        """
        Initialization of the user object

        :param str name: This is the users name
        :param str date_of_birth: This is the users date of birth in string format which gets converted to isoformat to be compatible across technologies
        :param str smoker: Represents if the user is a smoker or not
        :param str gender: The gender of the user
        """
        self._name = name
        self._date_of_birth = date_of_birth
        self._is_smoker = smoker
        self._gender = gender

    def __str__(self):
        """
        String representation of the User object
        :return: String output of the User object
        :rtype: str
        """

        if any(i is None for i in [self.name, self.date_of_birth, self.smoker, self.gender]):
            str_representation = ''
        else:
            smoker = 'smoker' if self._is_smoker else 'non-smoker'
            formatted_date_of_birth = parser.parse(self.date_of_birth).strftime('%d-%m-%Y')
            str_representation = '{name} was born on {date_of_birth} and is a {gender} {smoker}'.format(
                name=self.name.title(),
                date_of_birth=formatted_date_of_birth,
                gender=self.gender,
                smoker=smoker)

        return str_representation

    @property
    def name(self):
        """
        Gets the users name from the object

        :return: users name
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the users name on the object

        :param str name: The name of the user
        :return:
        :rtype: None
        """
        self._name = name

    @property
    def date_of_birth(self):
        """
        Gets the date of birth defined in the object

        :return: date of birth in isoformat
        :rtype: str
        """
        return self._date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, date_of_birth):
        """
        Sets the users date of birth on the object

        :param date_of_birth: String representation of the date of birth
        :return: date of birth in isoformat
        :rtype: str
        """
        try:
            # TODO: Could expand this to format all dates. Leaving this as the default type for now as it is the requirement
            formatted_date = dt.datetime.strptime(date_of_birth, '%d-%m-%Y')
        except Exception as e:
            logger.error('Exception while determining the DOB: {0}'.format(str(e)))
            raise e
        else:
            self._date_of_birth = formatted_date.isoformat()

    @property
    def smoker(self):
        """
        Gets whether or not the User is a smoker from the object

        :return: True is the user is a smoker. False if not
        :rtype: bool
        """
        return self._is_smoker

    @smoker.setter
    def smoker(self, is_smoker):
        """
        Sets whether or not the User is a smoker on the object

        :param str is_smoker: String representation of whether the user is a smoker or not.
        Yes for True. No for False
        :return:
        :rtype: None
        """

        if is_smoker.lower() in ['y', 'yes']:
            self._is_smoker = True
        elif is_smoker.lower() in ['n', 'no']:
            self._is_smoker = False
        else:
            raise TypeError('{0} is not a valid option for smoker'.format(is_smoker))

    @property
    def gender(self):
        """
        Gets the gender defined in the object

        :return:
        """
        return self._gender

    @gender.setter
    def gender(self, gender):
        """

        :param gender:
        :return:
        """
        if gender.lower() in ['male', 'female']:
            self._gender = gender
        else:
            raise TypeError('{0} is not a valid Gender'.format(gender))
