#!/usr/bin/env python3

import txc_helper

element = { 'RegularDayType':
               { 'DaysOfWeek':
                   { 'Monday': None,
                     'Tuesday': None,
                     'MondayToSaturday': None
                   }
               },
           'DaysOfNonOperation':
               { 'DateRange':
                   { 'StartDate': '2017-10-24',
                     'EndDate': '2017-10-30'
                   },
               },
           'BankHolidayOperation':
               { 'DaysOfNonOperation':
                   { 'AllBankHolidays': None
                   }
               }
          }

profile = txc_helper.OperatingProfile(element)

print(profile)
