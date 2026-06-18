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
# Custom player appearance columns
# ----------------------------

DONOR_COLUMNS = [
    "CAP_Hstl",
    "CAP_Hcol",
    "CAP_Hlen",
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
    "CAP_TRgtF",
    "EyeColor",
    "HParam1",
    "HParam2",
    "HdBrwHght",
    "HdBrwWdth",
    "HdBrwSlpd",
    "HdNkThck",
    "HdNkFat",
    "HdChnLen",
    "HdChnWdth",
    "HdChnProt",
    "HdJawSqr",
    "HdJawWdth",
    "HdChkHght",
    "HdChkWdth",
    "HdChkFull",
    "HdDefinit",
    "MtULCurve",
    "MtULThick",
    "MtULProtr",
    "MtLLCurve",
    "MtLLThick",
    "MtLLProtr",
    "MtSzHght",
    "MtSzWdth",
    "MtCrvCorn",
    "ErHeight",
    "ErWidth",
    "ErEarLobe",
    "ErTilt",
    "NsNsHght",
    "NsNsWdth",
    "NsNsProtr",
    "NsBnBridge",
    "NsBnDefin",
    "NsBnWdth",
    "NsTipHght",
    "NsTipWdth",
    "NsTipTip",
    "NsTipBnd",
    "NsNtHght",
    "NsNtWdth",
    "EsFrmOpen",
    "EsFrmSpac",
    "EsFrmLwEl",
    "EsFrmUpEl",
    "EsPlcHght",
    "EsPlcWdth",
    "EsPlcRot",
    "EsPlcProt",
    "EsShpOtEl",
    "EsShpInEl",
]

def check_compatability(pc, donor):
    if len(pc) != len(donor):
        raise ValueError(
            f"Row count mismatch: PC={len(pc)} donor={len(donor)}"
        )
    
    if len(pc.columns) != len(donor.columns):
        raise ValueError(
            f"Column count mismatch: PC={len(pc.columns)} donor={len(donor.columns)}"
        )
    
    for col in pc.columns:
        if col not in donor.columns:
            raise ValueError(
                f"PS3 CSV does not have {col} column!"
            )
        
    for col in donor.columns:
        if col not in pc.columns:
            raise ValueError(
                f"PC CSV does not have {col} column!"
            )


def convert(pc_csv, donor_csv, output_csv):

    pc = pd.read_csv(pc_csv, encoding="utf-16le")
    donor = pd.read_csv(donor_csv, encoding="utf-16le")

    check_compatability(pc, donor)

    # Force names to have no spaces for sake of importing
    pc['First_Name'] = pc["First_Name"].str.split().str.join('')
    pc['Last_Name'] = pc["Last_Name"].str.split().str.join('')


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

    pc.to_csv(output_csv, index=False, encoding="utf-16le")

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