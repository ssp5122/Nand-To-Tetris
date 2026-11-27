"""
Hack assembler (two-pass).
Student: Shresth Priyadarshi | Roll No: 2501420026 | K = 26
K-dependent feature: warn when a label is declared more than once.
Usage: python assembler.py Box.asm
"""
import re
import sys
from pathlib import Path

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
for i in range(16):
    PREDEFINED[f"R{i}"] = i

COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000",
    "!D": "0001101", "!A": "0110001",
    "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111",
    "D-1": "0001110", "A-1": "0110010",
    "D+A": "0000010", "D-A": "0010011", "A-D": "0000111",
    "D&A": "0000000", "D|A": "0010101",
}
# M computations use the same c-bits with the a-bit set to 1.
for mnemonic, bits in list(COMP.items()):
    if "A" in mnemonic:
        COMP[mnemonic.replace("A", "M")] = "1" + bits[1:]

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


def clean_line(raw):
    """Remove comments and insignificant whitespace."""
    return raw.split("//", 1)[0].replace(" ", "").replace("\t", "").strip()


def assemble(lines):
    """Return (machine_code, errors, warnings)."""
    symbols = dict(PREDEFINED)
    instructions = []
    errors = []
    warnings = []
    declared_labels = set()

    # Pass 1: strip comments, collect labels and instruction addresses.
    for line_number, raw in enumerate(lines, 1):
        line = clean_line(raw)
        if not line:
            continue

        if line.startswith("("):
            if not line.endswith(")") or not SYMBOL_RE.fullmatch(line[1:-1]):
                errors.append((line_number, f"invalid label '{line}'"))
                continue

            label = line[1:-1]
            if label in declared_labels:
                warnings.append((line_number, f"duplicate label '{label}'"))
                # Keep the first definition so references remain deterministic.
                continue
            if label in PREDEFINED:
                warnings.append((line_number, f"label '{label}' conflicts with a predefined symbol"))
                continue

            declared_labels.add(label)
            symbols[label] = len(instructions)
        else:
            instructions.append((line_number, line))

    # Pass 2: translate A- and C-instructions.
    output = []
    next_variable = 16

    for line_number, line in instructions:
        if line.startswith("@"):
            symbol_or_number = line[1:]
            if symbol_or_number.isdigit():
                value = int(symbol_or_number)
                if value > 32767:
                    errors.append((line_number, f"number too large '{line}' (maximum is 32767)"))
                    continue
            elif SYMBOL_RE.fullmatch(symbol_or_number):
                if symbol_or_number not in symbols:
                    symbols[symbol_or_number] = next_variable
                    next_variable += 1
                value = symbols[symbol_or_number]
            else:
                errors.append((line_number, f"invalid A-instruction '{line}'"))
                continue

            output.append(format(value, "016b"))
            continue

        # Parse dest=comp;jump, allowing either optional part.
        if line.count("=") > 1 or line.count(";") > 1:
            errors.append((line_number, f"invalid C-instruction '{line}'"))
            continue

        dest = ""
        jump = ""
        computation = line

        if "=" in computation:
            dest, computation = computation.split("=", 1)
        if ";" in computation:
            computation, jump = computation.split(";", 1)

        if dest not in DEST:
            errors.append((line_number, f"invalid destination '{dest}'"))
        elif computation not in COMP:
            errors.append((line_number, f"invalid computation '{computation}'"))
        elif jump not in JUMP:
            errors.append((line_number, f"invalid jump '{jump}'"))
        else:
            output.append("111" + COMP[computation] + DEST[dest] + JUMP[jump])

    return output, errors, warnings


def main(argv=None):
    argv = sys.argv if argv is None else argv
    if len(argv) != 2 or not argv[1].lower().endswith(".asm"):
        print("Usage: python assembler.py Prog.asm")
        return 1

    source_path = Path(argv[1])
    try:
        source_lines = source_path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"Error: cannot read '{source_path}': {exc}")
        return 1

    machine_code, errors, warnings = assemble(source_lines)

    for line_number, message in warnings:
        print(f"Warning (line {line_number}): {message}")

    if errors:
        for line_number, message in errors:
            print(f"Line {line_number}: {message}")
        print(f"Assembly failed with {len(errors)} error(s). No .hack file written.")
        return 1

    output_path = source_path.with_suffix(".hack")
    output_path.write_text("\n".join(machine_code) + "\n", encoding="utf-8")
    print(f"OK: wrote {output_path} ({len(machine_code)} instructions)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
