#!/usr/bin/env python3

import txc_helper
import datetime

saturday_service = {
    'RegularDayType': {
        'DaysOfWeek': {
            'Saturday': None,
        }
    },
    'BankHolidayOperation': {
        'DaysOfNonOperation': {
            'ChristmasDay': None,
            'BoxingDay': None,
            'GoodFriday': None,
            'NewYearsDay': None,
            'EasterMonday': None
        }
    },
    'SpecialDaysOperation': {
        'DaysOfNonOperation': {
            'DateRange': [
                {
                    'StartDate': '2017-12-30',
                    'EndDate': '2017-12-30'
                }
            ]
        },
    },
}

monfri_service = {
    'RegularDayType': {
        'DaysOfWeek': {
            'MondayToFriday': None,
        }
    },
    'BankHolidayOperation': {
        'DaysOfNonOperation': {
            'ChristmasDay': None,
            'BoxingDay': None,
            'GoodFriday': None,
            'NewYearsDay': None,
            'EasterMonday': None
        }
    },
    'SpecialDaysOperation': {
        'DaysOfNonOperation': {
            'DateRange': [
                {
                    'StartDate': '2017-10-23',
                    'EndDate': '2017-10-27'
                }
            ]
        },
    },
}


saturday = txc_helper.OperatingProfile(saturday_service)
print(saturday)
assert(saturday.should_show(datetime.date(2017, 10, 28)))
assert(not saturday.should_show(datetime.date(2017, 10, 30)))
assert(not saturday.should_show(datetime.date(2017, 12, 30)))

monfri = txc_helper.OperatingProfile(monfri_service)
print(monfri)
assert(not monfri.should_show(datetime.date(2017, 10, 28)))
assert(monfri.should_show(datetime.date(2017, 10, 30)))
assert(not monfri.should_show(datetime.date(2017, 12, 25)))
assert(not monfri.should_show(datetime.date(2017, 10, 23)))
