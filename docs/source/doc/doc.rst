=============
Documentation
=============

This project provides a suite of scripts to work on GnuCash files stored in SQL (sqlite3 and Postgres, not tested in MySQL).

Report creation (Linux and Windows, python >=3.5)
=================================================

Installation & use
------------------

You first need to install the gnucash-utilities with::

    $ pip install gnucash-utilities

Once installed, you can add python reports to gnucash by adding python files of the form 'report_name-of-report.py'
to your $HOME/.gnucash folder.

Everytime a python report is added or the signature of the report function is modified
(change of report metadata, addition/change/removal of an option), you should
run the gc_report script::

  For windows
  $ gc_report

  For linux
  $ gc_report.py

This script generates the scheme wrapper around the python report (it has the same name
as the python report file but with a .scm extension) and register the report in the $HOME/.gnucash/config.user file.

A simple report
---------------

The simplest report has the form of

.. literalinclude:: ../../../report_example/report_simplest.py

The core reporting logic is defined in the function 'generate_report' that::

 1. is decorated with the 'report' decorator
 2. takes one argument 'book_url' which is the book URL
 3. takes optional arguments representing the report options
 4. returns a string with html. This html is what gnucash will display as the result of the report execution.

.. warning::

 The report system provided by the gnucash-utilities has currently no way to identify the book that is
 running in gnucash (this can be fixed if a guile function is able to return the gnucash URI of the currently opened book).
 Hence, it uses a hack. It will look in the registry (for windows) or dconf (for linux) to find the last opened file and uses
 this a the "active gnucash book" (ie the 'book_url' argument of the 'generate_report' function).

 This hack will fail a.o. if you work with multiple gnucash book at the same time.

A report with options
---------------------

If you want to define options for your report, you can do it with type annotations as in

.. literalinclude:: ../../../report_example/report_simplest_parameters.py

Each option is an additional argument to the 'generate_report' function with its type defined through python type annotations.

Options currently supported are:

 - date with DateOption
 - float with RangeOption
 - str with StringOption

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

  For windows
  $ gc_report_create name-of-report

  For linux
  $ gc_report_create.py name-of-report


Testing your report from the command line
-----------------------------------------

You can test a report by just running the 'report_name-of-report.py' python file and piping the options to it as::

 $ cat inputs | python report_name-of-report.py

with inputs being a file like

.. literalinclude:: ../../../report_example/report_inputs.txt

The inputs should be in line with the options required by the report.

How does it work ?
------------------

The python report mechanism works as following:

 - At report creation:

     1. user creates a report by writing a python script as $HOME/.gnucash/report_name.py
     2. users launches the gc_report command that:

        a. generates a scheme wrapper as $HOME/.gnucash/report_name.scm
        b. adds the report to the file $HOME/.gnucash/config.user to have it loaded at each start of gnucash

 - At runtime:

     1. gnucash starts, loads $HOME/.gnucash/config.user and registers the report declared in the .scm files
     2. user launches a python report
     3. the scheme wrapper is called and:

        a. it starts a python subprocess "python report_name.py"
        b. it retrieves and serialises each report option in the format "option_name|option_value" and pipes it to the standard input of the python subprocess
        c. the python subprocesses:

            a. deserialises the options => option arguments
            b. retrieves the "last open gnucash book" => book_url argument
            c. calls the generate_report function with the arguments which returns an HTML string
            d. prints the HTML stringto the standard output

        d. it retrieves the standard output of the python subprocess as the HTML output of the report
