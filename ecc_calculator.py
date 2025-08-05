# Copyright (c) 2025 Bowen

# The COMPLETE and CORRECT Parity Matrix, derived directly from the
# Syndrome Table provided in the documentation.
# The value at index `i` is the syndrome for a single-bit error in `Data[i]`.
CORRECT_PARITY_MATRIX = [
    # Data[0] to Data[15]
    0xf4, 0xf1, 0xec, 0xea, 0xe9, 0xe6, 0xe5, 0xe3,
    0xdc, 0xda, 0xd9, 0xd6, 0xd5, 0xd3, 0xce, 0xcb,
    # Data[16] to Data[31]
    0xb5, 0xb0, 0xad, 0xab, 0xa8, 0xa7, 0xa4, 0xa2,
    0x9d, 0x9b, 0x98, 0x97, 0x94, 0x92, 0x8f, 0x8a,
    # Data[32] to Data[47]
    0x75, 0x70, 0x6d, 0x6b, 0x68, 0x67, 0x64, 0x62,
    0x5e, 0x5b, 0x58, 0x57, 0x54, 0x52, 0x4f, 0x4a,
    # Data[48] to Data[63]
    0x34, 0x31, 0x2c, 0x2a, 0x29, 0x26, 0x25, 0x23,
    0x1c, 0x1a, 0x19, 0x16, 0x15, 0x13, 0x0e, 0x0b
]

# The fixed XOR offset, verified from the (data=0, ecc=0x22) case.
ECC_OFFSET = 0x22

def calculate_ecc(data_hex: str) -> str:
    """
    Calculates the 8-bit ECC for a 64-bit data word using the
    final, documentation-verified parity matrix.

    Args:
        data_hex: A 16-character hexadecimal string representing the 64-bit data.

    Returns:
        A 2-character hexadecimal string for the calculated 8-bit ECC.
    """
    if not isinstance(data_hex, str) or len(data_hex) != 16:
        raise ValueError("Input must be a 16-character hex string.")

    try:
        data_int = int(data_hex, 16)
    except ValueError:
        raise ValueError("Input string is not a valid hexadecimal number.")

    base_ecc = 0
    for i in range(64):
        if (data_int >> i) & 1:
            base_ecc ^= CORRECT_PARITY_MATRIX[i]

    final_ecc = base_ecc ^ ECC_OFFSET
    return f"{final_ecc:02x}"

def run_verification():
    """
    Verifies the ECC calculation against a set of known test cases.
    """
    print("--- Running ECC Verification ---")

    test_cases = {
        "0000000000000000": "22",
        "0000000000000001": "d6",
        "0000000000000002": "d3",
        "0000000000000003": "27",
        "0000000000000004": "ce",
        "0000000000000005": "3a",
        "0000000000000006": "3f",
        "0000000000000007": "cb",
        "0000000000000008": "c8",
        "000000000000000f": "21",
        "0000000000000010": "cb",
        "0000000000000011": "3f",
        "0000000000000012": "3a",
        "0000031300000293": "9f",
        "0000041300000393": "1e",
    }

    all_passed = True
    for data, expected_ecc in test_cases.items():
        calculated_ecc = calculate_ecc(data)
        if calculated_ecc.lower() == expected_ecc.lower():
            status = "PASS"
            print(f"Data: 0x{data} | Expected: 0x{expected_ecc} | Calculated: 0x{calculated_ecc} -> \033[92m{status}\033[0m")
        else:
            status = "FAIL"
            print(f"Data: 0x{data} | Expected: 0x{expected_ecc} | Calculated: 0x{calculated_ecc} -> \033[91m{status}\033[0m")
            all_passed = False

    print("-" * 65)
    if all_passed:
        print("\033[92mAll test cases passed successfully!\033[0m")
    else:
        print("\033[91mSome test cases failed. Please check the matrix and logic.\033[0m")
    print("-" * 65)

def main():
    """Main function to run the verification suite."""
    run_verification()

if __name__ == "__main__":
    main()