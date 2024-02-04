from typing import Generator
from pathlib import Path


def read_lines(filename: Path) -> Generator[str, None, None]:
    with open(filename, "r", encoding="utf-8") as file:
        for line in file:
            yield line


def search_string_in_file(filename: Path, search_string: str, strict: bool = False) -> int:
    score = 0

    for line in read_lines(filename=filename):
        if strict is False:
            search_string, line = search_string.lower(), line.lower()

        if search_string in line:
            score += 1

    return score


def main():
    homework_03_dir = Path(__file__).parent
    filename = homework_03_dir / "rockyou.txt"
    search_string = input("Enter the search string: ")
    result: int = search_string_in_file(filename=filename, search_string=search_string)

    print(f"Lines found: {result}")


if __name__ == "__main__":
    main()
