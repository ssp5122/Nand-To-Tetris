# Verification status

Student: Shresth Priyadarshi  
Roll number: 2501420026  
K: 26

## Completed locally

- `assembler.py` compiles the personalised `Box.asm`.
- Every generated machine-code line is 16 binary digits.
- The box start address is 17216 (`SCREEN + 32*26`).
- The box loop writes three words per row for 20 rows.
- The K-dependent duplicate-label warning is implemented and regression-tested.

## Still required on the course simulator

These are not marked as passed because the official simulator/test scripts have not been run in this environment:

- [ ] `CPU.hdl` with `CPU.tst`
- [ ] `Memory.hdl` with `Memory.tst`
- [ ] `Computer.hdl` with `ComputerAdd.tst`
- [ ] `Computer.hdl` with `ComputerMax.tst`
- [ ] `Computer.hdl` with `ComputerRect.tst`
- [ ] Load `Box.hack` in CPU Emulator and capture the box-while-key-pressed screenshot.
- [ ] Capture the cleared-box screenshot after releasing the key.
- [ ] Add genuine test screenshots to the 3–4 page report and submit it on ZOSIMA.

## Regression test

Run:

```bash
python -m unittest test_assembler.py
```
