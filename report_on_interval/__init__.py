def compute_reporting_interval(item_count):
    """
    Computes for a given number of items that will be processed how often the
    progress should be reported
    """
    if item_count > 100000:
        log_interval = item_count // 100
    elif item_count > 30:
        log_interval = item_count // 10
    else:
        log_interval = 1
    return log_interval


def report_on_interval(
        iterable,
        message='processed {i} of {n} items',
        item_count=None,
        printer=print,
        get_deltas=compute_reporting_interval,
        report_at_end=False,
        extra_actions=[],
        extras_at_end=False,
):
    """
    Provides a generator of items from an iterable that prints a status report
    on a regular interval as items are produced. May also execute extra actions
    at each reporting interval

    :param: iterable:      The iterable to loop over
    :param: message:       The formatted message to print (special vars: i, n)
                           i: the index of the current iteration (+1)
                           n: the total number of iterations
    :param: item_count:    The number of items in the iterable. If None, the
                           iterable will be converted to a list so that the
                           len() method can be applied to get the item count.
                           NOTE: letting this method compute the item count
                           will hurt performance when a generator is passed as
                           the iterable (if the iterable is large)
    :param: printer:       The method used to print messages. Defaults to
                           ``print`` directed to stdout.
    :param: get_deltas:    Function to compute interval for reporting.
                           Defaults to compute_reporting_interval().
                           Should take the count of items in the iterable as
                           the only argument.
    :param: report_at_end: Include a reporting message after the last iteration
                           Will only occur if n is not a multiple of delta
    :param: extra_actions: Other functions to execute on the interval. Should
                           be an iterable of callables (functions) that take no
                           arguments.
    :param: extras_at_end: Execute extra actions after last iteration
                           Will only occur if n is not a multiple of delta

    :Example:

    >>> for entry in report_on_interval(some_stuff):
    ...     do_something()
    processed 30 of 300 items
    processed 60 of 300 items
    processed 90 of 300 items
    ...
    """
    if item_count is not None:
        n = item_count
    else:
        iterable = list(iterable)
        n = len(iterable)
    delta = get_deltas(n)
    for (i, item) in enumerate(iterable):
        yield item
        if (i + 1) % delta == 0:
            printer(message.format(i=i + 1, n=n))
            [a() for a in extra_actions]
    if n % delta != 0:
        if report_at_end:
            printer(message.format(i=n, n=n))
        if extras_at_end:
            [a() for a in extra_actions]
