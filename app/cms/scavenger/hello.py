import argparse


def main(n):
    return n ** 2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Square any number.")
    parser.add_argument("number", metavar="n", type=int, help="number to be squared")

    args = parser.parse_args()

    result = main(args.number)

    print(result)
