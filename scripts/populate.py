import json
import datetime
import math
import os
import traceback
import django
import pandas as pd

###############
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_crud.settings')
django.setup()
###############


from homes.models import DayShift, Home, MonthlyShiftAggregate, WeeklyShiftAggregate
from users.models import BondableUser


def populate(day_input):
    # read from xlsx
    df: pd.DataFrame = pd.read_excel(
        "/Users/dipeshpandey/experiments/bondable/bondable_raw/scripts/test_sheet3.xlsx",
        skiprows=4,
    )
    records_str = df.to_json(orient="records")
    records = json.loads(records_str)
    for record in records:
        print(record["Ops Mgr"], record["Home"])
        if not record["Ops Mgr"] or not record["Home"]:
            continue
        try:
            ops_mgr, created = BondableUser.objects.get_or_create(
                name=record["Ops Mgr"],
                username=record["Ops Mgr"].replace(" ", "_").lower(),
                type="OPS_MGR",
            )
            home, created = Home.objects.get_or_create(
                name=record["Home"], lead_contact=ops_mgr
            )
            home.registered_beds = record["Registered Beds"]
            home.effective_beds = record["Effective Beds"]
            home.budget = record["Budget"]
            home.save()
            # create a day shift
            day = datetime.datetime.date(datetime.datetime.strptime(day_input, "%Y-%m-%d"))
            day_shift, created = DayShift.objects.get_or_create(home=home, day=day)
            day_shift.occupancy_percent = record["Occupancy %"]
            day_shift.occupancy = math.ceil(record["Occupancy %"] * home.effective_beds)

            day_shift.admissions_week_to_date = record["Admissions"]
            day_shift.deaths_week_to_date = record["Deaths"]
            day_shift.discharges_week_to_date = record["Discharges"]
            day_shift.live_enquiries = record["Live Enq"]

            # day_shift.hours_worked = record[""]
            day_shift.hours_worked_from_home_in_last_24_hours = record[
                "Hours Worked in Home(Last 24 Hours)"
            ]
            # day_shift.agency_hours_in_last_24_hours =
            day_shift.agency_hours_in_last_24_hours_carer = record[
                "Agency (Last 24 Hours) - Carer"
            ]
            day_shift.agency_hours_in_last_24_hours_nurse = record[
                "Agency (Last 24 Hours) - Nurse"
            ]
            day_shift.agency_hours_in_last_24_hours_senior_carer = record[
                "Agency (Last 24 Hours) - Senior Carer"
            ]

            day_shift.save()

            # create a weekly shift aggregate
            # get week number from date
            week = day_shift.day.isocalendar().week
            (
                weekly_shift_aggregate,
                created,
            ) = WeeklyShiftAggregate.objects.get_or_create(
                home=home, week_number=week, year=day_shift.day.year
            )
            weekly_shift_aggregate.occupancy = day_shift.occupancy * 7
            weekly_shift_aggregate.planned_admissions = record["Planned Admissions"]
            weekly_shift_aggregate.planned_discharges = record["Planned Discharges"]
            weekly_shift_aggregate.expected_end_of_life = record["Expected End of Life"]
            weekly_shift_aggregate.agency_nurse_hours = record[
                "Agency (Last 24 Hours) - Nurse"
            ]
            weekly_shift_aggregate.agency_carer_hours = record[
                "Agency (Last 24 Hours) - Carer"
            ]
            weekly_shift_aggregate.agency_senior_carer_hours = record[
                "Agency (Last 24 Hours) - Senior Carer"
            ]
            weekly_shift_aggregate.save()

            # create a monthly shift aggregate
            # get human readable month name from date
            month = day_shift.day.strftime("%B")
            (
                monthly_shift_aggregate,
                created,
            ) = MonthlyShiftAggregate.objects.get_or_create(
                home=home, month=month, year=day_shift.day.year
            )
            monthly_shift_aggregate.occupancy = day_shift.occupancy * 30
            monthly_shift_aggregate.nurse_hours = record["Monthly Nurse"]
            monthly_shift_aggregate.carer_hours = record["Monthly Carer"]

            monthly_shift_aggregate.save()

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            break


populate("2023-02-08")
