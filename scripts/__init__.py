import subprocess


def format():
    subprocess.run(["black", "."])
    subprocess.run(["isort", "."])
