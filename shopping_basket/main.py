import argparse


def main():
    pass


ap = argparse.ArgumentParser()

ap.add_argument("-t", "--test", required=False, default=False, help="Execute all unit tests")

args = vars(ap.parse_args())


if __name__ == '__main__':
    if args["test"]:
        pass
    else:
        main()
