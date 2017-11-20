import os


# def get_latest_file():
#     if sys.platform.startswith("win"):
#         try:
#             import winreg
#         except ImportError:
#             import _winreg as winreg
#
#         explorer = winreg.OpenKey(
#             winreg.HKEY_CURRENT_USER,
#             "Software\\GSettings\\org\\gnucash\\history"
#         )
#         value, type = winreg.QueryValueEx(explorer, "file0")
#         return value
#     elif sys.platform.startswith("linux"):
#         import subprocess
#         output_dconf = subprocess.check_output(["dconf", "dump", "/org/gnucash/history/"]).decode()
#         from configparser import ConfigParser
#         conf = ConfigParser()
#         conf.read_string(output_dconf)
#         return conf["/"]["file0"][1:-1]
#     else:
#         raise NotImplemented("not yet implemented for sys.platform = '{}'".format(sys.platform))


def get_user_config_path():
    from os.path import expanduser
    home = expanduser("~")

    potential_paths = [
        (os.path.join(home, "AppData", "Roaming", "GnuCash"), "2.7"),
        (os.path.join(home, "AppData", "Local", "GnuCash"), "2.7"),
        (os.path.join(home, ".gnucash"), "2.6"),
    ]

    for p, v in potential_paths:
        if os.path.exists(p):
            return p, v

    raise FileNotFoundError("Could not not found the GnuCash user folder after having looked in:\n"
                            "{}".format("\n".join(potential_paths)))


def update_config_user(lines, separator=";; lines automatically added\n;; everything below this line will be scraped"):
    # add the list of lines to the end of the config.user file
    # separating the original content and the new content
    # through a separator
    user_config_path, version= get_user_config_path()
    path = os.path.join(user_config_path, "config.user")
    if os.path.exists(path):
        with open(path, "r") as fin:
            original = fin.read()
    else:
        original = ""

    if separator in original:
        original = original[:original.index(separator)]

    if not original.endswith("\n"):
        original += "\n"

    original += separator + "\n"
    original += "\n".join(lines)

    with open(path, "w") as fout:
        fout.write(original)
