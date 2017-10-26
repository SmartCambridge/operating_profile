import calendar
import datetime
import pprint

WEEKDAYS = {day: i for i, day in enumerate(calendar.day_name)}
BANK_HOLIDAYS = {
    datetime.date(2016, 12, 26): ('BoxingDay',),
    datetime.date(2017, 4, 14): ('GoodFriday',),
    datetime.date(2017, 4, 17): ('EasterMonday', 'HolidayMondays'),
    datetime.date(2017, 5, 1): ('MayDay', 'HolidayMondays'),
    datetime.date(2017, 5, 29): ('SpringBank', 'HolidayMondays'),
    datetime.date(2017, 8, 7): ('AugustBankHolidayScotland',),
    datetime.date(2017, 8, 28): ('LateSummerBankHolidayNotScotland', 'HolidayMondays'),
    datetime.date(2017, 12, 24): ('ChristmasEve',),
    datetime.date(2017, 12, 25): ('ChristmasDay', 'ChristmasDayHoliday'),
    datetime.date(2017, 12, 26): ('BoxingDay',),
    datetime.date(2018, 1, 1): ('NewYearsDay', 'NewYearsDayHoliday'),
    datetime.date(2018, 3, 30): ('GoodFriday',),
    datetime.date(2018, 4, 2): ('EasterMonday', 'HolidayMondays'),
    datetime.date(2018, 5, 7): ('MayDay', 'HolidayMondays'),
    datetime.date(2018, 5, 28): ('SpringBank', 'HolidayMondays'),
    datetime.date(2018, 8, 6): ('AugustBankHolidayScotland',),
    datetime.date(2017, 8, 27): ('LateSummerBankHolidayNotScotland',),
}

class DayOfWeek(object):
    def __init__(self, day):
        if isinstance(day, int):
            self.day = day
        else:
            self.day = WEEKDAYS[day]

    def __eq__(self, other):
        if type(other) == int:
            return self.day == other
        return self.day == other.day

    def __repr__(self):
        return calendar.day_name[self.day]

class DateRange(object):
    # Use this to represent the object that will later be stored in the database as a DateRangeField
    # https://docs.djangoproject.com/en/1.11/ref/contrib/postgres/fields/#django.contrib.postgres.fields.DateRangeField
    def __init__(self, element):
        self.start = datetime.datetime.strptime(element['StartDate'], '%Y-%m-%d').date()
        self.end = datetime.datetime.strptime(element['EndDate'], '%Y-%m-%d').date()

    def contains(self, date):
        return self.start <= date and (not self.end or self.end >= date)


class OperatingProfile(object):
    def __init__(self, element, servicedorgs):

        self.regular_days = []
        self.nonoperation_days = []
        self.operation_days = []
        self.nonoperation_bank_holidays = []
        self.operation_bank_holidays = []

        if 'RegularDayType' in element and 'DaysOfWeek' in element['RegularDayType']:
            week_days_element = element['RegularDayType']['DaysOfWeek']
            for day in list(week_days_element.keys()):
                if 'To' in day:
                    day_range_bounds = [WEEKDAYS[i] for i in day.split('To')]
                    day_range = range(day_range_bounds[0], day_range_bounds[1] + 1)
                    self.regular_days += [DayOfWeek(i) for i in day_range]
                elif day == 'Weekend':
                    self.regular_days += [DayOfWeek(5), DayOfWeek(6)]
                else:
                    self.regular_days.append(DayOfWeek(day))

        # Special Days:
        if 'SpecialDaysOperation' in element:
            if 'DaysOfNonOperation' in element['SpecialDaysOperation']:
                self.nonoperation_days = list(map(DateRange, element['SpecialDaysOperation']['DaysOfNonOperation']['DateRange']))
            if 'DaysOfOperation' in element['SpecialDaysOperation']:
                self.operation_days = list(map(DateRange, element['SpecialDaysOperation']['DaysOfOperation']['DateRange']))

        # Bank Holidays
        if 'BankHolidayOperation' in element:
            if 'DaysOfNonOperation' in element['BankHolidayOperation']:
                self.nonoperation_bank_holidays = list(element['BankHolidayOperation']['DaysOfNonOperation'].keys())
            else:
                self.nonoperation_bank_holidays = []
            if 'DaysOfOperation' in element['BankHolidayOperation']:
                self.operation_bank_holidays = list(element['BankHolidayOperation']['DaysOfOperation'].keys())
            else:
                self.operation_bank_holidays = []

    def __repr__(self):
        return (pprint.pformat(self.regular_days) +
            pprint.pformat(self.nonoperation_days) +
            pprint.pformat(self.operation_days) +
            pprint.pformat(self.nonoperation_bank_holidays) +
            pprint.pformat(self.operation_bank_holidays))

    def should_show(self, date):
        if self.regular_days:
            if date.weekday() not in self.regular_days:
                return False
        if date in BANK_HOLIDAYS:
            if 'AllBankHolidays' in self.operation_bank_holidays:
                return True
            if 'AllBankHolidays' in self.nonoperation_bank_holidays:
                return False
            for bank_holiday in BANK_HOLIDAYS[date]:
                if bank_holiday in self.operation_bank_holidays:
                    return True
                if bank_holiday in self.nonoperation_bank_holidays:
                    return False
        if not self.regular_days and not hasattr(self, 'operation_days'):
            return False

        if hasattr(self, 'nonoperation_days'):
            for daterange in self.nonoperation_days:
                if daterange.contains(date):
                    return False

        if hasattr(self, 'operation_days'):
            for daterange in self.operation_days:
                if daterange.contains(date):
                    return True
            return False

        return True

    def defaults_from(self, defaults):
        '''
        Merge this object with a second one containing defaults according to the rules in the schema guide.    
        '''
        pass
