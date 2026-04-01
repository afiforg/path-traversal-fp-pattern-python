# Path Traversal False-Positive Pattern (Python)

This project intentionally demonstrates a control-flow pattern that can trigger a taint-analysis false positive:

- Source: `--path` CLI flag (`input_path`)
- Guard: `if input_path != "": return input_path`
- Sink: `open(...)` appears later in the same function path

The key detail: the sink executes only when `input_path == ""`.
So there is no runtime path where a non-empty attacker-controlled `--path` value reaches `open`.

## Run

```bash
cd path-traversal-fp-pattern-python
python3 main.py --path "../../../../etc/passwd"
```

Expected output:

```text
resolved path: ../../../../etc/passwd
```

No file read is performed in this case because the function returns at the guard.

Now run with an empty path:

```bash
python3 main.py
```

Expected output:

```text
resolved path: ./safe-default/location
```

In this case, `open("fixtures/default_path.txt")` is executed, but no attacker-controlled path is involved.
