import pandas as pd
import argparse

# ----------------------------
# Columns that PS3 expects to have fixed values
# ----------------------------

FIXED_VALUES = {
    "CF_ID": 0,
    "Overall_I": 0,
    "NickName": 0,
    "AudioID_M": 0
}

# ----------------------------
# CAP appearance columns
# ----------------------------

CAP_COLUMNS = [
    "CAP_Hstl",
    "CAP_Hcol",
    "CAP_BStyle",
    "CAP_Moust",
    "CAP_Goatee",
    "CAP_Fhcol",
    "CAP_Eyebr",

    "CAP_TLftN",
    "CAP_TLftS",
    "CAP_TRgtS",
    "CAP_TLftB",
    "CAP_TRgtB",
    "CAP_TLftF",
]

# ----------------------------
# Face/head morph columns
# (add every morph slider here)
# ----------------------------

HEAD_COLUMNS = [
    "HdBrwHght",
    "HdBrwWdth",
    "HdBrwSlpd",

    # Add all remaining Hd*
    # Eye*
    # Nose*
    # Chin*
    # Jaw*
    # Ear*
    # Mouth*
    # Cheek*
    # etc.
]

DONOR_COLUMNS = CAP_COLUMNS + HEAD_COLUMNS


def convert(pc_csv, donor_csv, output_csv):

    pc = pd.read_csv(pc_csv, encoding="utf-16le")
    donor = pd.read_csv(donor_csv, encoding="utf-16le")

    if len(pc) != len(donor):
        raise ValueError(
            f"Row count mismatch: PC={len(pc)} donor={len(donor)}"
        )

    # Force PS3 values
    for col, value in FIXED_VALUES.items():
        if col in pc.columns:
            pc[col] = value

    # Copy donor appearance
    for col in DONOR_COLUMNS:

        if col not in pc.columns:
            print(col + " not in PC columns.")
            continue

        if col not in donor.columns:
            print (col + " not in donor columns.")
            continue

        pc[col] = donor[col].values

    pc.to_csv(output_csv, index=False)

    print(f"Saved {output_csv}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("pc_csv")
    parser.add_argument("donor_csv")
    parser.add_argument("output_csv")

    args = parser.parse_args()

    convert(
        args.pc_csv,
        args.donor_csv,
        args.output_csv
    )