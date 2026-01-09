from __future__ import annotations

from pathlib import Path
from io import StringIO
import re
import pandas as pd


def parse_xfoil_polar_txt(path: str | Path) -> pd.DataFrame:
    """
    Parse an XFOIL polar text file (like your output) into a clean DataFrame.
    Output columns: alpha_deg, CL, CD, (optional CM), Re, Mach, airfoil
    """
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    # --- Extract metadata (Mach, Re, Airfoil) from header if available
    airfoil = None
    mach = None
    reynolds = None

    for line in lines:
        # "Calculated polar for: NACA 2412"
        if "Calculated polar for:" in line:
            airfoil = line.split("Calculated polar for:")[-1].strip()

        # "Mach =   0.200     Re =     1.000 e 6"
        if "Mach" in line and "Re" in line and ("=" in line):
            m = re.search(r"Mach\s*=\s*([0-9.]+)", line)
            r = re.search(r"Re\s*=\s*([0-9.]+)\s*e\s*([0-9]+)", line)
            if m:
                mach = float(m.group(1))
            if r:
                base = float(r.group(1))
                exp = int(r.group(2))
                reynolds = base * (10 ** exp)

    # --- Find the table header line starting with "alpha"
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("alpha"):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not find table header line starting with 'alpha'.")

    # Skip the dashed separator line (next line)
    data_start = header_idx + 2

    table_text = "\n".join(lines[header_idx:data_start]) + "\n" + "\n".join(lines[data_start:])
    df = pd.read_csv(StringIO("\n".join(lines[header_idx:data_start - 1] + lines[data_start:])),
                     sep=r"\s+")

    # Standardize names
    rename = {}
    for c in df.columns:
        cl = c.strip().lower()
        if cl == "alpha":
            rename[c] = "alpha_deg"
        elif cl == "cl":
            rename[c] = "CL"
        elif cl == "cd":
            rename[c] = "CD"
        elif cl == "cm":
            rename[c] = "CM"
    df = df.rename(columns=rename)

    # Keep what we need (CM optional)
    keep = [c for c in ["alpha_deg", "CL", "CD", "CM"] if c in df.columns]
    df = df[keep].copy()

    # Add metadata columns
    if reynolds is not None:
        df["Re"] = float(reynolds)
    if mach is not None:
        df["Mach"] = float(mach)
    if airfoil is not None:
        df["airfoil"] = airfoil

    # Drop any weird rows
    df = df.dropna()
    return df
