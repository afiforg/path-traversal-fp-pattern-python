import sys

from anchors import pick_base_reference


COMMANDS: dict[str, callable] = {}


def cli_command(name: str):
    def decorator(func):
        COMMANDS[name] = func
        return func

    return decorator


def parse_option(args: list[str], option: str, default: str = "") -> str:
    if option in args:
        idx = args.index(option)
        if idx + 1 < len(args):
            return args[idx + 1]
        raise ValueError(f"missing value for {option}")
    return default


def resolve_resource_path(input_path: str) -> str:
    # Demonstrates the same false-positive pattern:
    # - If user input is non-empty, return immediately.
    # - open() only executes when input_path == "".
    # - input_path still flows into sink argument construction.
    if input_path != "":
        return input_path

    return pick_base_reference(input_path)


@cli_command("resolve")
def resolve_command(path: str = "") -> None:
    try:
        result = resolve_resource_path(path)
    except OSError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(1)

    print(f"resolved path: {result}")


def main() -> None:
    args = sys.argv[1:]
    command_name = "resolve"
    if args and not args[0].startswith("-"):
        command_name = args[0]
        args = args[1:]

    command = COMMANDS.get(command_name)
    if command is None:
        print(f"unknown command: {command_name}", file=sys.stderr)
        raise SystemExit(2)

    try:
        path = parse_option(args, "--path", default="")
    except ValueError as err:
        print(f"error: {err}", file=sys.stderr)
        raise SystemExit(2)

    command(path=path)


if __name__ == "__main__":
    main()
