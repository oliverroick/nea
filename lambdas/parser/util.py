from datetime import date, timedelta


today = date.today()
week_start = today - timedelta(days=8)
week_end = today - timedelta(days=1)


def is_recent(item):
    date = item['date']
    return week_start <= date and date <= week_end


def serialisable(item):
    item['date'] = str(item['date'])
    return item
