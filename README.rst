.. image::  https://badge.fury.io/py/report-on-interval.svg
   :target: https://badge.fury.io/py/report-on-interval
   :alt:    Latest Published Version

.. image::  https://travis-ci.org/dusktreader/report-on-interval.svg?branch=master
   :target: https://travis-ci.org/dusktreader/report-on-interval
   :alt:    Build Status

********************
 report-on-interval
********************

---------------------------------------------------------
Print out regular status reports while looping over items
---------------------------------------------------------

This package provides a function that simply prints out information about the
progress of a loop that iterates over an iterable. So, say you have a 10k
elements that you are iterating over and each one takes a second. Wouldn't it
be nice to get a little output after every 1% of the items are processed?

With report-on-interval, it's as easy as this:

.. code-block:: python:

   from report_on_interval import report_on_interval

   for item in report_on_interval(lots_of_items):
       do_something_with_item(item)

Output would look like this::

   processed 100 of 10000 items
   processed 200 of 10000 items
   processed 300 of 10000 items
   processed 400 of 10000 items
   ...
   processed 10000 of 10000 items


Super-quick Start
-----------------
 - requirements: `python` versions 3.4+
 - install through pip: `$ pip install report-on-interval`

Additional Options
------------------

The ``report_on_interval`` function has some additional arguments that may be
useful:

* ``message``

  Supply your own message for the report:

  .. code-block:: python:

      for bug in report_on_interval(
              bug_generator,
              message='{i}/{n} little buggers squished',
      ):
          squash_bug(bug)

* ``item_count``

  If you are looping over an iterator that produces items programatically, you
  absolutely should provide this if you know the total number of items.
  Otherwise, ``report_on_interval`` will convert the iterable to a list, and,
  poof!, the benefits of programatically producing items disapears. A great
  example of this is iterating over the results from a SQLAlchemy query:

  .. code-block:: python:

      query = session.query(MyModel).filter(MyModel.column > 0)
      for row in report_on_interval(
              query,
              item_count=query.count(),
      ):
          process_row(row)

* ``printer``

  Supply a different printer than the default of printing to standard out. This
  is often an application logger:

  .. code-block:: python:

      from my_app.logging import logger
      for cheese in report_on_interval(cheese_shop, printer=logger):
          request_cheese(cheese)

* ``get_deltas``

  Provide your own method for computing the reporting interval. By default,
  the ``compute_reporting_interval`` method is used. This method prints
  after every 1% is processed for iterables with over 100k items, after every
  10% for iterables over 30 items, and after every item for anything else

  .. code-block:: python:

      def deltafier(n):
          return n // 7
      for marble in report_on_interval(bag, get_deltas=deltafier):
          shoot(marble)

* ``report_at_end``

  Print the progress report after the last item is processed. Maybe you want
  a report when your loop is done because you don't report it yourself. There's
  no accounting for tastes...

* ``extra_actions``

  Provide a list of additional tasks to perform on each reporting interval.
  One use for this is to regularly flush updates out to your database on the
  interval as well as reporting  progress

  .. code-block:: python:

      for new_thingie in report_on_interval(
          produce_new_thingies,
          item_count=thingie_total,
          extra_actions=[lambda: session.flush()],
      ):
          thingie.update(doodad=None)

* ``extras_at_end``

  Also perform the extra actions after finishing the loop. Note that like the
  ``report_at_end`` argument, if the count of items in the iterable is an exact
  multiple of the reporting interval, this will not result in an extra report
  and running the extras a second time. The logic in ``report_on_interval``
  makes sure of that
