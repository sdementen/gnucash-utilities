import hashlib
import inspect
import os
import sys
import traceback

import sqlalchemy

from .options import Option

template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "templates"))


class Report:
    name = ""
    title = ""
    options = None
    function = None
    menu_tip = ""
    python_script = None

    def __init__(self, name, title, menu_tip, options, options_default_section, function=None, python_script=None):
        self.name = name
        self.title = title
        self.menu_tip = menu_tip

        self.options = [] if options is None else options
        self.options_default_section = options_default_section
        if function:
            self.function = function
        if python_script:
            self.python_script = python_script

    @property
    def guid(self):
        """
        """
        return hashlib.sha224("{}-{}".format(self.name, self.title).encode('utf-8')).hexdigest()

    def generate_scm(self):
        import jinja2
        scm_view = jinja2.Template(retrieve_template_scm()).render(
            project=self,
            python_interpreter='"' + repr("'" + sys.executable)[2:].replace("python.exe", "pythonw.exe"),
        )
        return scm_view


def retrieve_template_scm():
    """
    """
    with open(os.path.join(template_path, "python_report_template.scm")) as f:
        return f.read()


def generate_sample_report_python():
    with open(os.path.join(template_path, "report_example.py")) as f:
        return f.read()


def generate_sample_report_html():
    with open(os.path.join(template_path, "report_example.html")) as f:
        return f.read()


def report(options_default_section,
           title,
           name,
           menu_tip,
           ):
    options = []
    p = Report(options_default_section=options_default_section,
               title=title,
               name=name,
               menu_tip=menu_tip,
               options=options,
               )

    def process_function(f):
        fsig = inspect.signature(f)

        for name, param in fsig.parameters.items():
            if isinstance(param.annotation, Option):
                param.annotation.name = name
                options.append(param.annotation)

        def wrapped(book_url):
            dct = {}
            input_options = sys.stdin.readlines()
            for option, option_meta in zip(input_options, options):
                var, value = option.split("|")
                dct[var] = option_meta.parse(value)

            # convert path given by gnucash to URI usable by piecash
            book_url = (book_url
                        .replace("file://", "sqlite:///")
                        # .replace("postgres://", "postgres:///")
                        .replace("mysql://", "mysql+pymysql://")  # to use pymysql instead of
                        )

            return f(book_url, **dct)

        wrapped.project = p
        return wrapped

    return process_function


def output_trace_html(exc_info):
    # report the trace in html output
    mystdout = os.fdopen(sys.stdout.fileno(), 'w')
    original_write = mystdout.write
    original_write('<html><head><style>pre {font-family: arial;}</style></head><body>')

    def wrapped_write(text):
        text = "".join("<pre>{}</pre>".format(l) for l in text.split("\n"))
        original_write(text)

    mystdout.write = wrapped_write
    traceback.print_exception(*exc_info, file=mystdout)
    original_write("</body></html>")
    mystdout.flush()



def execute_report(generate_report, book_url):
    try:
        s = generate_report(book_url)
        print(s)
    except sqlalchemy.exc.DatabaseError as e:
        print("File {} is not an sqlite file. Check that you saved your gnucash book with the sqlite3 data format.".format(book_url))
    except Exception as e:
        exc_info = sys.exc_info()
        output_trace_html(exc_info)
