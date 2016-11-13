#!/usr/bin/env python
import glob
import os
import sys

from piecash_utilities import update_config_user, get_user_config_path

if sys.version_info >= (3,0):
    import importlib


    def load_module(file_path):
        return importlib.machinery.SourceFileLoader("mod", file_path).load_module()
else:
    import imp


    def load_module(file_path):
        return imp.load_source("mod", file_path)


def main():
    lines_report = []
    user_path = get_user_config_path()
    for p in glob.glob(os.path.join(user_path, "report_*.py")):
        path_name, ext = os.path.splitext(p)
        name = os.path.basename(path_name)
        mod = load_module(p)

        if hasattr(mod, "generate_report"):
            project = mod.generate_report.project
            project.python_script = name + ext

            scm_view = project.generate_scm()
            scm_name = name + ".scm"
            print("generate", name)
            with open(os.path.join(user_path, scm_name), "w") as f:
                f.write(scm_view)
            lines_report.append('(load (gnc-build-dotgnucash-path "{}"))'.format(scm_name))

    update_config_user(lines_report)


if __name__ == '__main__':
    main()
