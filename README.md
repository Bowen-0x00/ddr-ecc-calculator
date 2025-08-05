# DDR ECC Calculator

A simple Python tool to calculate the 8-bit Error-Correcting Code (ECC) for a 64-bit data word. The calculation is based on the specific syndrome/parity matrix used by many common DDR controllers, such as those from Cadence.

## Background

In high-reliability systems, DDR memory controllers often employ ECC to detect and correct memory errors. A common implementation is a SECDED (Single Error Correction, Double Error Detection) Hamming code, which adds 8 bits of ECC to every 64 bits of data.

This tool implements the ECC generation logic for one such standard. The core of this logic is the `CORRECT_PARITY_MATRIX`, which defines how each data bit contributes to the final ECC value. This matrix was derived directly from the syndrome table found in the technical documentation for Cadence DDR PHYs.

## Features

-   Calculates an 8-bit ECC for a 64-bit data input.
-   Uses an industry-standard parity matrix for DDR ECC.
-   Includes a self-verification suite with known test cases to ensure correctness.
-   Written in simple, dependency-free Python.

## How It Works

The ECC calculation is performed using a linear-feedback shift register (LFSR) model, which can be simplified to the following steps:

1.  Initialize a `base_ecc` variable to `0`.
2.  Iterate through each of the 64 bits of the input data.
3.  If a data bit is `1`, XOR the corresponding 8-bit value from the `CORRECT_PARITY_MATRIX` into the `base_ecc`.
4.  After iterating through all 64 bits, XOR the `base_ecc` with a final `ECC_OFFSET` (in this case, `0x22`) to get the final ECC value. This offset accounts for the case where the input data is all zeros.

## Usage

The script is self-contained and primarily serves as a verification tool. To run the verification suite, simply execute the Python script:

```bash
python ecc_calculator.py