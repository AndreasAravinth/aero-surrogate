from __future__ import annotations

from pathlib import Path
from io import StringIO
import re
import pandas as pd


def parse_xfoil_polar_txt(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()

    airfoil = None
    naca_code = None
    mach = None
    reynolds = None
    ncrit = None

    for line in lines:
        if "Calculated polar for:" in line:
            airfoil = line.split("Calculated polar for:")[-1].strip()
            m_naca = re.search(r"NACA\s*([0-9]{4,5})", airfoil, re.IGNORECASE)
            if m_naca:
                naca_code = int(m_naca.group(1))

        if "Mach" in line and "Re" in line and ("=" in line):
            m = re.search(r"Mach\s*=\s*([0-9.]+)", line)
            r = re.search(r"Re\s*=\s*([0-9.]+)\s*e\s*([0-9]+)", line)
            n = re.search(r"Ncrit\s*=\s*([0-9.]+)", line)
            if m:
                mach = float(m.group(1))
            if r:
                base = float(r.group(1))
                exp = int(r.group(2))
                reynolds = base * (10 ** exp)
            if n:
                ncrit = float(n.group(1))

    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("alpha"):
            header_idx = i
            break
    if header_idx is None:
        raise ValueError("Could not find table header line starting with 'alpha'.")

    data_start = header_idx + 2

    df = pd.read_csv(
        StringIO("\n".join(lines[header_idx:data_start - 1] + lines[data_start:])),
        sep=r"\s+"
    )

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

    keep = [c for c in ["alpha_deg", "CL", "CD", "CM"] if c in df.columns]
    df = df[keep].copy()

    if reynolds is not None:
        df["Re"] = float(reynolds)
    if mach is not None:
        df["Mach"] = float(mach)
    if ncrit is not None:
        df["Ncrit"] = float(ncrit)
    if airfoil is not None:
        df["airfoil"] = airfoil
    if naca_code is not None:
        df["naca"] = int(naca_code)

    return df.dropna()
