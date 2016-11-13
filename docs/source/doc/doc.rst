=============
Documentation
=============

This project provides a suite of scripts to work on GnuCash files stored in SQL (sqlite3 and Postgres, not tested in MySQL).

Report creation (Linux and Windows, python 3.X)
===============================================

Installation & use
------------------

You first need to install the gnucash-utilities.

Once installed, you can add python reports to gnucash by adding python files of the form 'report_name-of-report.py'
to your $HOME/.gnucash folder.
Everytime a python report is added or the signature of the report functions is modified
(change of report metadata, addition/change/removal of an option), you should
run the 'gc_report' (for windows) or 'gc_report.py' (for linux) script.
This script generates the scheme wrappers around the python report.

A simple report
---------------

The simplest report has the form of

.. literalinclude:: ../../../report_example/report_simplest.py

It is a function 'generate_report' that::

 1. is decorated with the 'report' decorator
 2. take one argument 'book_url' which is the book URL
 3. take optional arguments representing the report options
 4. and that returns a string with html. This html is what gnucash will display as the result of the report execution.

.. warning::

 The report system provided by the gnucash-utilities has currently no way to identify the book that is
 running in gnucash (this could be fixed if a guile function is able to return the gnucash URI). Hence, it uses
 a hack. It will look in the registry (for windows) or dconf (for linux) to find the last opened file and uses
 this a the "active gnucash book" (ie the 'book_url' argument of the 'generate_report' function).

 This hack will fail if you work with multiple gnucash book at the same time.

A report with options
---------------------

If you want to define options for your report, you can do it with type annotations as in

.. literalinclude:: ../../../report_example/report_simplest_parameters.py

Each option is an additional argument to the 'generate_report' function with its type defined through python type annotations.

A report that access the book
-----------------------------

Most of the report will want to access the gnucash book. You can use piecash to open the book thanks to the 'book_url' argument
that the 'generate_report' function gets automatically as illustrated in the following example

.. literalinclude:: ../../../report_example/report_simplest_book.py


A full fledged example with jinja2 to generate the html
-------------------------------------------------------

You can use the command 'gc_create_report name-of-report' (under windows) or 'gc_create_report.py name-of-report' (under linux)
to create a set of files 'report_name-of-report.py' and 'report_name-of-report.html' that use the jinja2 templating logic to
generate the report. For any moderately complex report, this is the suggested approach.

You can also generate a sample file automatically by executing::

  $ gc_report_create whatyouwant

  $ gc_report_create.py whatyouwant


Testing your report from the command line
-----------------------------------------

You can test a report by just running the 'report_name-of-report.py' python file and piping the options to it as::

 $ cat inputs | python report_name-of-report.py

with inputs being a file like

.. literalinclude:: ../../../report_example/report_inputs.txt

