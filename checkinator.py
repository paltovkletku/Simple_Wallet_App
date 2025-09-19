from datetime import datetime
from exceptions import *

#  миксин для проверки инпутов
class ValueCheck:

    def is_cost_valid(self, cost):
        try:
            if float(cost) < 0:
                raise NegativeCost
        except (ValueError, NegativeCost):
            return False
        return True

    def is_date_valid(self, date):
        try:
            if date == 't':
                date = datetime.today().strftime('%d.%m.%Y')
            if (datetime.strptime(date, '%d.%m.%Y') < datetime(1974, 1, 1)
                    or datetime.strptime(date, '%d.%m.%Y') > datetime.today()):
                raise IncorrectDate
        except (ValueError, IncorrectDate):
            return False
        return True

    def is_name_valid(self, name):
        if (not name) or (not name.strip()):
            return False
        return True

    def is_date_appropriate(self, date, app_date):
        if date.day != int(app_date):
            return False
        return True

    def is_length_valid(self, name):
        try:
            if len(name) > 100:
                raise LengthError
        except LengthError:
            return False
        return True


    def is_balance_valid(self, balance):
        try:
            if balance < 0:
                raise NegativeBalance
        except NegativeBalance:
            return False
        return True


    def is_summa_valid(self, summa):
        try:
            if float(summa) < 0:
                raise IncorrectTopUp
        except (IncorrectTopUp, ValueError):
            return False
        return True
