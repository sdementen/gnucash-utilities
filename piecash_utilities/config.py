import os
import sys


def get_latest_file():
    if sys.platform.startswith("win"):
        try:
            import winreg
        except ImportError:
            import _winreg as winreg

        explorer = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            "Software\\GSettings\\org\\gnucash\\history"
        )
        value, type = winreg.QueryValueEx(explorer, "file0")
        return value
    elif sys.platform.startswith("linux"):
        import subprocess
        output_dconf = subprocess.check_output(["dconf", "dump", "/org/gnucash/history/"]).decode()
        from configparser import ConfigParser
        conf = ConfigParser()
        conf.read_string(output_dconf)
        return conf["/"]["file0"][1:-1]
    else:
        raise NotImplemented("not yet implemented for sys.platform = '{}'".format(sys.platform))


def get_user_config_path():
    from os.path import expanduser
    home = expanduser("~")
    if sys.platform.startswith("win") or sys.platform.startswith("linux"):
        return os.path.join(home, ".gnucash")
    else:
        raise NotImplemented("not yet implemented for sys.platform = '{}'".format(sys.platform))


def update_config_user(lines, separator=";; lines automatically added\n;; everything below this line will be scraped"):
    # add the list of lines to the end of the config.user file
    # separating the original content and the new content
    # through a separator
    path = os.path.join(get_user_config_path(), "config.user")
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