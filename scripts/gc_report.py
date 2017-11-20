#!/usr/bin/env python
import glob
import os
import sys

from piecash_utilities import update_config_user, get_user_config_path

if sys.version_info >= (3, 0):
    import importlib


    def load_module(file_path):
        return importlib.machinery.SourceFileLoader("mod", file_path).load_module()
else:
    import imp


    def load_module(file_path):
        return imp.load_source("mod", file_path)


def main():
    lines_report = []
    user_path, version = get_user_config_path()
    scm_user_path = "gnc-build-userdata-path" if version == "2.7" else "gnc-build-dotgnucash-path"
    lines_report.append("(define gnc-build-dotgnucash-path {})".format(scm_user_path))
    for p in glob.glob(os.path.join(user_path, "report_*/")):
        # p is a folder $GNUCASH_USER_FOLDER/name_of_report/
        # name = name_of_report
        _, name = os.path.split(os.path.dirname(p))

        # load the module $GNUCASH_USER_FOLDER/name_of_report/name_of_report.py
        mod = load_module(os.path.join(p, name + ".py"))

        if hasattr(mod, "generate_report"):
            project = mod.generate_report.project
            project.python_script = os.path.join(name, name + ".py")

            scm_view = project.generate_scm()
            scm_name = name + ".scm"
            print("generate", name)
            with open(os.path.join(user_path, name, scm_name), "w") as f:
                f.write(scm_view)
            lines_report.append('(load ({scm_user_path} "{scm_name}"))'.format(
                scm_user_path=scm_user_path,
                scm_name=os.path.join(name, scm_name).replace("\\","/")))

    update_config_user(lines_report)


if __name__ == '__main__':
    main()
