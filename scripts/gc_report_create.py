import os
import shutil
import sys

from piecash_utilities import generate_sample_report_html
from piecash_utilities import generate_sample_report_python
from piecash_utilities import get_user_config_path


def main():
    if len(sys.argv) <= 1:
        print("provide a name for your report")
        sys.exit(1)
    name_report_base = sys.argv[1]
    name_report = "report_" + name_report_base + ".py"
    name_html =  "report_" + name_report_base + ".html"

    path_report = os.path.join(get_user_config_path(), name_report)
    path_html = os.path.join(get_user_config_path(), name_html)

    if os.path.exists(path_report):
        print("file '{}' already exist, will not overwrite it".format(path_report))
        sys.exit(1)

    with open(path_report, "w") as f:
        f.write(generate_sample_report_python().replace("NAMEOFREPORT", name_report_base))
    with open(path_html, "w") as f:
        f.write(generate_sample_report_html())


    print("file '{}' successfully created".format(path_report))


if __name__ == '__main__':
    main()
