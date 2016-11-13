import ast
import datetime

import jinja2


class Option:
    type = ""
    section = ""
    name = ""
    sort_tag = ""
    documentation_string = ""
    default_value = ""

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
        return jinja2.Template("""
            (op-value "{{option.section}}" "{{option.name}}")""").render(option=self)

    def parse(self, value):
        return ast.literal_eval(value)


class DateOption(Option):
    def __init__(self, is_datetime=False, **kwargs):
        super(DateOption, self).__init__(type="gnc:make-date-option", **kwargs)
        self.is_datetime = is_datetime

    def render_serialise(self):
        return jinja2.Template("""
            (cadr (op-value "{{option.section}}" "{{option.name}}"))
            """).render(option=self)

    def parse(self, value):
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
        return jinja2.Template("""    (add-option
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

    def parse(self, value):
        return value