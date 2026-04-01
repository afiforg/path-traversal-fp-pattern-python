import sys

import click

from anchors import pick_base_reference


def resolve_resource_path(input_path: str) -> str:
    # Demonstrates the same false-positive pattern:
    # - If user input is non-empty, return immediately.
    # - open() only executes when input_path == "".
    # - input_path still flows into sink argument construction.
    if input_path != "":
        return input_path

    return pick_base_reference(input_path)


@click.command()
@click.option("--path", "input_path", default="", help="user-provided path")
def main(input_path: str) -> None:
    try:
        result = resolve_resource_path(input_path)
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(1)

    print(f"resolved path: {result}")


if __name__ == "__main__":
    main()
