from report_on_interval import report_on_interval


def test_report_on_interval(self):
    accumulator = []
    for item in report_on_interval(
            range(101),
            message='{i} / {n}',
            printer=lambda m: accumulator.append(m),
            report_at_end=True,
            extra_actions=[
                lambda: accumulator.append('extra1'),
                lambda: accumulator.append('extra2'),
            ],
            extras_at_end=True,
    ):
        accumulator.append(item)

    assert accumulator == [
        *range(0, 10),
        '10 / 101',
        'extra1',
        'extra2',
        *range(10, 20),
        '20 / 101',
        'extra1',
        'extra2',
        *range(20, 30),
        '30 / 101',
        'extra1',
        'extra2',
        *range(30, 40),
        '40 / 101',
        'extra1',
        'extra2',
        *range(40, 50),
        '50 / 101',
        'extra1',
        'extra2',
        *range(50, 60),
        '60 / 101',
        'extra1',
        'extra2',
        *range(60, 70),
        '70 / 101',
        'extra1',
        'extra2',
        *range(70, 80),
        '80 / 101',
        'extra1',
        'extra2',
        *range(80, 90),
        '90 / 101',
        'extra1',
        'extra2',
        *range(90, 100),
        '100 / 101',
        'extra1',
        'extra2',
        100,
        '101 / 101',
        'extra1',
        'extra2',
    ]

    accumulator = []
    for item in report_on_interval(
            range(25),
            message='{i} / {n}',
            printer=lambda m: accumulator.append(m),
            get_deltas=lambda n: 5,
            report_at_end=True,
    ):
        accumulator.append(item)

    assert accumulator == [
        *range(0, 5),
        '5 / 25',
        *range(5, 10),
        '10 / 25',
        *range(10, 15),
        '15 / 25',
        *range(15, 20),
        '20 / 25',
        *range(20, 25),
        '25 / 25',
    ]
