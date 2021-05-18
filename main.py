import sys
import pytest
from app import execute


def run():
    execute()
    pass


def test():
    pytest.main(args=["."])
    pass


def install():
    # TODO: install requirements.txt
    pass


def prepare():
    # TODO: prepare env
    pass


def init():
    # TODO: source env/bin/activate
    pass


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "run":
        run()
    elif sys.argv[1] == "test":
        test()
    elif sys.argv[1] == "install":
        install()
    elif sys.argv[1] == "prepare":
        prepare()
    elif sys.argv[1] == "init":
        init()
else:
    print("Please run this script individually")
