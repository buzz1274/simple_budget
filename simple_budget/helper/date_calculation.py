from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from simple_budget.settings import START_DATE
import calendar


class DateCalculation(object):
    """
    date calculations used withing simple budget
    """

    @staticmethod
    def calculate_years(year=None):
        try:
            year = int(year)
        except TypeError:
            year = None

        if not year:
            return [None, None, None]
        else:
            today = datetime.now()

            if year + 1 <= today.year:
                next_year = year + 1
            else:
                next_year = None

            if year - 1 >= datetime.strptime(START_DATE, '%Y-%m-%d').year:
                prev_year = year - 1
            else:
                prev_year = None

            return [year, next_year, prev_year]

    @staticmethod
    def calculate_dates(year_month=None):
        """
        :param year_month:
        :return: prev_month, next_month, start_date, end_date
        """
        today = datetime.now()
        start_date = date(datetime.now().year, datetime.now().month, 1)
        end_date = date(datetime.now().year, datetime.now().month,
                        calendar.monthrange(datetime.now().year,
                                            datetime.now().month)[1])

        next_month = date(today.year, today.month, 1) + \
                     relativedelta(months=1)
        prev_month = date(today.year, today.month, 1) - \
                     relativedelta(months=1)

        if year_month:
            try:
                year_month = datetime.strptime(year_month, '%Y-%m')
            except ValueError:
                year_month = None

            if year_month:
                start_date = date(year_month.year, year_month.month, 1)
                if (START_DATE and
                    (datetime.strptime(str(start_date), '%Y-%m-%d') <
                     datetime.strptime(START_DATE, '%Y-%m-%d')) or
                    (datetime.strptime(str(start_date), '%Y-%m-%d') >
                     datetime.now())):
                    start_date = None
                else:
                    today = start_date
                    end_date = date(year_month.year, year_month.month,
                                    calendar.monthrange(year_month.year,
                                                        year_month.month)[1])
                    next_month = date(year_month.year, year_month.month, 1) + \
                                 relativedelta(months=1)
                    prev_month = date(year_month.year, year_month.month, 1) - \
                                 relativedelta(months=1)

        if (START_DATE and
            datetime.strptime(str(prev_month), '%Y-%m-%d') <
            datetime.strptime(START_DATE, '%Y-%m-%d')):
            prev_month = None

        if next_month > date(datetime.now().year, datetime.now().month,
                             datetime.now().day):
            next_month = None

        return [prev_month, next_month, start_date, end_date, today]