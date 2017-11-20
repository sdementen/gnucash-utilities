import ast
import datetime

import jinja2
from piecash import Commodity


class Option:
    """An option to be used in a report

    Attributes:
        type (str): the type of the option of the form 'gnc:make-number-range-option'
        section (str): the section/tab where the option should appear in the option dialog
        sort_tag (str): a string defining the sort order in the tab
        documentation_string (str): the doc string of the option
        default_value (str): the default value of the option
        name (str): the name of the variable
    """
    def __init__(self, type, section, sort_tag, documentation_string, default_value, name=None):
        self.type = type
        self.section = section
        self.name = name
        self.sort_tag = sort_tag
        self.documentation_string = documentation_string
        self.default_value = default_value

    def render_scheme(self):
        pass

    def render_serialise(self):
        return jinja2.Template("""(op-value "{{option.section}}" "{{option.name}}")""").render(option=self)

    def parse(self, value, book):
        return ast.literal_eval(value)


class DateOption(Option):
    def __init__(self, is_datetime=False, **kwargs):
        super(DateOption, self).__init__(type="gnc:make-date-option", **kwargs)
        self.is_datetime = is_datetime

    def render_serialise(self):
        return jinja2.Template("""(cadr (op-value "{{option.section}}" "{{option.name}}"))""").render(option=self)

    def parse(self, value, book):
        return datetime.datetime.fromtimestamp(ast.literal_eval(value))

    def render_scheme(self):
        return jinja2.Template("""    (add-option
       ({{ option.type }}
      (N_ "{{option.section}}") (N_ "{{option.name}}")
      "{{option.sort_tag}}" (N_ "{{option.documentation_string}}")
      {{option.default_value}}  ;; default
      #f 'absolute #f
      ))
        """).render(option=self)


class RangeOption(Option):
    def __init__(self, lower=0, upper=10000, decimals=2, step_size=0.01, **kwargs):
        super(RangeOption, self).__init__(type="gnc:make-number-range-option", **kwargs)
        self.lower = lower
        self.upper = upper
        self.decimals = decimals
        self.step_size = step_size

    def render_scheme(self):
        return jinja2.Template("""(add-option
       ({{ option.type }}
      (N_ "{{option.section}}") (N_ "{{option.name}}")
      "{{option.sort_tag}}" (N_ "{{option.documentation_string}}")
      {{option.default_value}}  ;; default
      {{option.lower }}     ;; lower bound
      {{option.upper }} ;; upper bound
      {{option.decimals }}     ;; number of decimals
      {{option.step_size }}    ;; step size
      ))
        """).render(option=self)


class StringOption(Option):
    def __init__(self, **kwargs):
        super(StringOption, self).__init__(type="gnc:make-string-option", **kwargs)

    def render_scheme(self):
        return jinja2.Template("""    (add-option
       ({{ option.type }}
      (N_ "{{option.section}}") (N_ "{{option.name}}")
      "{{option.sort_tag}}" (N_ "{{option.documentation_string}}")
      "{{option.default_value}}"  ;; default
      ))
        """).render(option=self)

    def parse(self, value, book):
        return value

class CommodityOption(Option):
    def __init__(self, **kwargs):
        super(CommodityOption, self).__init__(type="gnc:make-commodity-option",
                                              **kwargs)

    def render_scheme(self):
        return jinja2.Template("""    (add-option
       ({{ option.type }}
      (N_ "{{option.section}}") (N_ "{{option.name}}")
      "{{option.sort_tag}}" (N_ "{{option.documentation_string}}")
      {{option.default_value}}  ;; default
      ))
        """).render(option=self)

    def render_serialise(self):
        return jinja2.Template(
            '(string-append (gnc-commodity-get-namespace (op-value "{{option.section}}" "{{option.name}}"))'
            ' ">" '
            '(gnc-commodity-get-mnemonic (op-value "{{option.section}}" "{{option.name}}")))').render(option=self)

    def parse(self, value, book):
        namespace, mnemonic = value.strip('"').split(">")
        return book.commodities(namespace=namespace, mnemonic=mnemonic)
