from datetime import date, timedelta


today = date.today()
two_weeks_ago = today - timedelta(days=8)


def is_recent(item):
    d = today - timedelta(days=3)
    if item['date']:
        d = item['date']
    return two_weeks_ago <= d and d <= today


def serialisable(item):
    item['date'] = str(item['date'])
    return item
