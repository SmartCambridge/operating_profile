#!/usr/bin/env python3

import txc_helper
import datetime
import xml.etree.ElementTree as ET

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
            'DateRange': {
                'StartDate': '2017-12-30',
                'EndDate': '2017-12-30'
            }
        },
    },
}

saturday_service_et = ET.fromstring('''
      <OperatingProfile xmlns="http://www.transxchange.org.uk/">
        <RegularDayType>
          <DaysOfWeek>
            <Saturday />
          </DaysOfWeek>
        </RegularDayType>
        <SpecialDaysOperation>
          <DaysOfNonOperation>
            <DateRange>
              <StartDate>2017-12-30</StartDate>
              <EndDate>2017-12-30</EndDate>
            </DateRange>
          </DaysOfNonOperation>
        </SpecialDaysOperation>
        <BankHolidayOperation>
          <DaysOfNonOperation>
            <ChristmasDay />
            <BoxingDay />
            <GoodFriday />
            <NewYearsDay />
            <EasterMonday />
          </DaysOfNonOperation>
        </BankHolidayOperation>
      </OperatingProfile>
    ''')

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
                },
                {
                    'StartDate': '2018-10-23',
                    'EndDate': '2018-10-27'
                }
            ]
        },
    },
}

monfri_service_et = ET.fromstring('''
      <OperatingProfile xmlns="http://www.transxchange.org.uk/">
        <RegularDayType>
          <DaysOfWeek>
            <MondayToFriday />
          </DaysOfWeek>
        </RegularDayType>
        <SpecialDaysOperation>
          <DaysOfNonOperation>
            <DateRange>
              <StartDate>2017-10-23</StartDate>
              <EndDate>2017-10-27</EndDate>
            </DateRange>
            <DateRange>
              <StartDate>2018-12-23</StartDate>
              <EndDate>2018-10-27</EndDate>
            </DateRange>
          </DaysOfNonOperation>
        </SpecialDaysOperation>
        <BankHolidayOperation>
          <DaysOfNonOperation>
            <ChristmasDay />
            <BoxingDay />
            <GoodFriday />
            <NewYearsDay />
            <EasterMonday />
          </DaysOfNonOperation>
        </BankHolidayOperation>
      </OperatingProfile>
    ''')

saturday = txc_helper.OperatingProfile.from_list(saturday_service)
print(saturday)
assert(saturday.should_show(datetime.date(2017, 10, 28)))
assert(not saturday.should_show(datetime.date(2017, 10, 30)))
assert(not saturday.should_show(datetime.date(2017, 12, 30)))

saturday_xml = txc_helper.OperatingProfile.from_et(saturday_service_et)
print(saturday_xml)
assert(saturday_xml.should_show(datetime.date(2017, 10, 28)))
assert(not saturday_xml.should_show(datetime.date(2017, 10, 30)))
assert(not saturday_xml.should_show(datetime.date(2017, 12, 30)))

monfri = txc_helper.OperatingProfile.from_list(monfri_service)
print(monfri)
assert(not monfri.should_show(datetime.date(2017, 10, 28)))
assert(monfri.should_show(datetime.date(2017, 10, 30)))
assert(not monfri.should_show(datetime.date(2017, 12, 25)))
assert(not monfri.should_show(datetime.date(2017, 10, 23)))

monfri_xml = txc_helper.OperatingProfile.from_et(monfri_service_et)
print(monfri_xml)
assert(not monfri_xml.should_show(datetime.date(2017, 10, 28)))
assert(monfri_xml.should_show(datetime.date(2017, 10, 30)))
assert(not monfri_xml.should_show(datetime.date(2017, 12, 25)))
assert(not monfri_xml.should_show(datetime.date(2017, 10, 23)))


empty = txc_helper.OperatingProfile()
print(empty)
empty.defaults_from(saturday)
print(empty)

#j = saturday.to_json()
#print(j)
#saturday2 = OperatingProfile.from_json(j)
#print(saturday2)
