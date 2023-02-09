import argparse
import concurrent.futures
import logging
import multiprocessing
import pathlib
import string
import time
from collections.abc import Iterator
from math import ceil
from typing import NamedTuple, Final

from custom_logger import CustomFormatter

# logger initialization
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)


# Create paths for writing into a file
current_path = pathlib.Path(__file__).parent  # get current directory
output = current_path.joinpath("output")  # create "output" subdirectory


# Quantity of cores
CPUs = multiprocessing.cpu_count()


class ActionArgs(NamedTuple):
    alphabet: str
    number_of_start_word: int
    word_length: int
    start_word_as_digits: list[int]
    word: str
    package_number: int


def generate_words_for_current_package(
    alphabet: str,
    number_of_start_word: int,
    word_length: int,
    start_word_as_digits: list[int],
    word: str,
    package_number: int,
) -> list[str]:
    list_of_package_words = []
    for _ in range(amount_of_items_in_package):
        word_as_digits = list(
            convert_decimal_number_to_custom_base(
                number=number_of_start_word, base=alphabet_length, word_length=word_length
            )
        )
        word = "".join([alphabet[character_index] for character_index in word_as_digits])
        number_of_start_word += 1
        list_of_package_words.append(word)
        if word == alphabet[-1] * word_length:
            break
    write_to_file(list_of_package_words=list_of_package_words, file=package_number)
    return list_of_package_words


def __wrapper(args: ActionArgs) -> list[str]:
    logger.debug(f"{args=}")
    return generate_words_for_current_package(**args._asdict())


def convert_decimal_number_to_custom_base(number: int, base: int, word_length: int) -> Iterator[int]:

    list_of_numbers_to_convert = [0 for _ in range(word_length)]
    counter = word_length - 1
    number_to_convert = number

    while number_to_convert:
        floor_division, remainder = divmod(number_to_convert, base)
        list_of_numbers_to_convert[counter] = remainder
        number_to_convert = floor_division
        counter -= 1

    return list_of_numbers_to_convert


def write_to_file(list_of_package_words: list, file):
    with open(f"{output}/package {file}.txt", "w") as f:
        for word in list_of_package_words:
            f.write(f"{word}\n")


def main(word_length, alphabet):
    packages = [
        ActionArgs(
            alphabet=alphabet,
            number_of_start_word=amount_of_items_in_package * package_number,
            word_length=word_length,
            start_word_as_digits=list(
                convert_decimal_number_to_custom_base(
                    number=amount_of_items_in_package * package_number, base=alphabet_length, word_length=word_length
                )
            ),
            word="".join(
                [
                    alphabet[character_index]
                    for character_index in list(
                        convert_decimal_number_to_custom_base(
                            number=amount_of_items_in_package * package_number,
                            base=alphabet_length,
                            word_length=word_length,
                        )
                    )
                ]
            ),
            package_number=package_number,
        )
        for package_number in range(amount_of_packages)
    ]
    with concurrent.futures.ProcessPoolExecutor(CPUs) as executor:
        executor.map(
            __wrapper,
            packages,
        )


if __name__ == "__main__":
    CustomFormatter()

    alphabet = string.ascii_lowercase + string.digits
    alphabet_length = len(alphabet)

    parser = argparse.ArgumentParser(description="Fuzz generator")
    parser.add_argument("-word_len", type=int, help="Input length of word", required=False, default=5)
    args = parser.parse_args()

    total_number_of_words: Final[int] = len(alphabet) ** args.word_len
    amount_of_items_in_package = 1_000_000
    amount_of_packages = ceil(total_number_of_words / amount_of_items_in_package)

    start = time.perf_counter()
    logger.warning(f"{alphabet=}, {args.word_len=}, {total_number_of_words=}")
    main(word_length=args.word_len, alphabet=alphabet)
    elapsed = time.perf_counter() - start
    logger.warning(f"Program completed in {elapsed:0.5f} seconds.")
    logger.warning(f"Total generated words: {total_number_of_words} Total generated packages: {amount_of_packages}")
    logger.info(f"All data written to files in f'{output}")
