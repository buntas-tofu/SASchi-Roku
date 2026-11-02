"""Candidate translation of the supplied, self-contained SAS DATA step.

Source attribution supplied with source.sas:
https://rosettacode.org/wiki/Sum_and_product_of_an_array
Page revision 408601; GFDL 1.2 (Rosetta_Code:Copyrights).
Retrieved 2026-09-08T14:05:31Z.

Scope: logical PUT records, excluding physical SAS log layout and diagnostics.
"""

import math


def execute_data_step() -> tuple[float, float]:
    """Return the two numeric values named by PUT in this source program."""
    a = [math.nan] * 100
    i = 1.0
    while i <= 100.0:
        a[int(i) - 1] = i * i
        i += 1.0

    # Every element is assigned before SUM executes in this bounded source.
    b = sum(a)
    c = math.nan
    return b, c


def main() -> None:
    b, c = execute_data_step()
    # This source prints an exact integer and an ordinary numeric missing value.
    print(f"{b:.0f}", "." if math.isnan(c) else f"{c:.0f}")


if __name__ == "__main__":
    main()
