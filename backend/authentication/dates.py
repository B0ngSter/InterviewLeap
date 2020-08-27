from itertools import groupby
from django.db import connections
from monthdelta import monthdelta
import operator
import datetime

def months(startdate):
    """Yield all months since start"""
    date = datetime.date(startdate.year, startdate.month, 1)
    while True:
        yield date
        date = date + monthdelta(1)

def combine(grouped, startdate, date_field):
    """
        Combine the grouped items with a list of dates from startdate
        So grouped should be [(date, items), ...]
        And startdate is a date object.
    """
    step = 0
    for date in months(startdate):
        if step == len(grouped):
            return

        _, things = grouped[step]
        compare = getattr(things[0], date_field)

        if compare.year == date.year and compare.month == date.month:
            step += 1
            yield date, list(things)
        else:
            yield date, []


def by_month(model, date_field, startdate=None):
    """Return a list of [(month, objects), ...]"""
    results = list(model.extra(select={'month':connections[model.db].ops.date_trunc_sql('month',
                                                                                        date_field)}).order_by('month'))

    if not startdate:
        startdate = getattr(results[0], date_field)

    grouped = [(nxt, list(things)) for nxt, things in groupby(results, operator.attrgetter('month'))]
    return combine(grouped, startdate, date_field)