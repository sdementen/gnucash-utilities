import hashlib
import inspect
import os
import sys

from piecash_utilities.config import get_latest_file
from .options import Option



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
        return hashlib.sha224("{}-{}".format(self.name, self.title).encode('utf-8')).hexdigest()

    def generate_scm(self):
        import jinja2

        env = jinja2.Environment(loader=jinja2.PackageLoader(__name__, '.'))
        scm_view = env.get_template("python_report_template.scm").render(
            project=self,
            python_interpreter='"' + repr("'" + sys.executable)[2:].replace("python.exe","pythonw.exe"),
        )
        return scm_view


def generate_sample_report_python():
    with open(os.path.join(os.path.dirname(__file__),"report_example.py")) as f:
        return f.read()

def generate_sample_report_html():
    with open(os.path.join(os.path.dirname(__file__),"report_example.html")) as f:
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

        def wrapped():
            dct = {}
            input_options = sys.stdin.readlines()
            for option, option_meta in zip(input_options, options):
                var, value = option.split("|")
                dct[var] = option_meta.parse(value)

            book_url = get_latest_file()
            return f(book_url, **dct)

        wrapped.project = p
        return wrapped

    return process_function
