def get_date():
    for y in range(2018, 2022):
        for m in range(1, 13):
            _date = str(y) + str(m)
            if m < 10:
                _date = str(y) + '0' + str(m)
            yield _date

