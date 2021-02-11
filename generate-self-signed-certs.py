"""
Script to generate self signed SSL certificates
"""

from datetime import timedelta
import os
from typing import Any

import argparse

parser = argparse.ArgumentParser(description="Generate self signed SSL certificates")

args = parser.parse_args()

_defaults = {
    "CERT_STORAGE_DIR": "self_signed_cert",
    "CERT_FILENAME": "server.crt",
    "KEY_FILENAME": "server.key",
}


class Defaults(object):
    def __init__(self, defaults: dict) -> None:
        self.defaults = defaults

    def __getattribute__(self, name: str) -> Any:
        defaults = object.__getattribute__(self, "defaults")
        return defaults.get(name, None)


defaults = Defaults(_defaults)

# Change directory to ndserver root
os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.chdir("..")

try:
    os.mkdir(defaults.CERT_STORAGE_DIR)
except FileExistsError:
    pass
finally:
    print(f"Created certificate storage directory : {defaults.CERT_STORAGE_DIR}")

os.chdir(defaults.CERT_STORAGE_DIR)

# os.system("apt install --yes openssl")

validity_period_years = 100
validity_period = timedelta(days=365 * validity_period_years)

key_subjects = {
    "country": "IN",
    "state": "HP",
    "locality": "Hamirpur",
    "organisation": "Team ISTE",
    "domain_name": "abhedya-server",
}

subject_prop_map = {
    "country": "C",
    "state": "ST",
    "locality": "L",
    "organisation": "O",
    "domain_name": "CN",
}


subject_string = "".join(
    [
        f"/{subject_prop_map[param]}={key_subjects[param]}"
        for param in key_subjects.keys()
    ]
)

os.system(
    f'openssl req \
        -newkey rsa:4906\
        -x509\
        -nodes\
        -sha256\
        -days {validity_period.days}\
        -newkey rsa:4096\
        -keyout ./{defaults.KEY_FILENAME}\
        -out ./{defaults.CERT_FILENAME}\
        -subj "{subject_string}"'
)

print(
    f"Created certificate {os.path.join(defaults.CERT_STORAGE_DIR,defaults.CERT_FILENAME)} and key {os.path.join(defaults.CERT_STORAGE_DIR,defaults.KEY_FILENAME)}"
)

print("DONE")
