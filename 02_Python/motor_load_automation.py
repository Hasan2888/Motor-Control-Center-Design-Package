"""
Motor Load Calculation Automation
==================================
Automates the same three calculations done manually in the Excel workbook:
  1. Motor Load Schedule  -> FLA lookup (NEC Table 430.250)
  2. Cable Sizing          -> 125% rule (NEC 430.22)
  3. Panel / Breaker Sizing -> 250% rule (NEC 430.52)

Project: Electrical Design Package - Small Commercial Building MCC
"""

from dataclasses import dataclass
from typing import List, Tuple
import csv

# ------------------------------------------------------------------
# Reference tables (same source data as the Excel workbook)
# ------------------------------------------------------------------

# NEC Table 430.250 - Full-Load Current (FLA) for 3-phase, 460V motors (A)
FLA_TABLE_460V = {
    1: 2.1, 1.5: 3, 2: 3.4, 3: 4.8, 5: 7.6, 7.5: 11,
    10: 14, 15: 21, 20: 27, 25: 34, 30: 40, 40: 52, 50: 65,
}

# NEC Table 310.16 - Conductor ampacity, 75C copper (A), ascending order
CABLE_AMPACITY_TABLE: List[Tuple[str, int]] = [
    ("14 AWG", 20), ("12 AWG", 25), ("10 AWG", 35), ("8 AWG", 50),
    ("6 AWG", 65), ("4 AWG", 85), ("3 AWG", 100), ("2 AWG", 115),
    ("1 AWG", 130), ("1/0 AWG", 150),
]

# Standard breaker sizes (A), ascending order
BREAKER_SIZES: List[int] = [
    15, 20, 25, 30, 35, 40, 45, 50, 60, 70,
    80, 90, 100, 110, 125, 150, 175, 200, 225, 250,
]


# ------------------------------------------------------------------
# Motor definition
# ------------------------------------------------------------------

@dataclass
class Motor:
    """One motor entry - mirrors a row in the Excel Motor Load Schedule."""
    motor_id: str
    description: str
    location: str
    hp: float
    voltage: int = 460
    phase: int = 3

    @property
    def fla(self) -> float:
        """Full-load amps, looked up from NEC Table 430.250."""
        if self.hp not in FLA_TABLE_460V:
            raise ValueError(f"No FLA entry for {self.hp} HP - add it to FLA_TABLE_460V.")
        return FLA_TABLE_460V[self.hp]


# ------------------------------------------------------------------
# Sizing logic (equivalent to the INDEX/MATCH formulas in Excel)
# ------------------------------------------------------------------

def select_cable_size(fla: float) -> Tuple[str, int]:
    """Smallest conductor whose ampacity >= 125% of FLA (NEC 430.22)."""
    min_ampacity = fla * 1.25
    for awg, ampacity in CABLE_AMPACITY_TABLE:
        if ampacity >= min_ampacity:
            return awg, ampacity
    raise ValueError("FLA exceeds the largest conductor in the table.")


def select_breaker_size(fla: float) -> int:
    """Smallest standard breaker >= 250% of FLA (NEC 430.52)."""
    max_protection = fla * 2.5
    for size in BREAKER_SIZES:
        if size >= max_protection:
            return size
    raise ValueError("FLA exceeds the largest breaker in the table.")


# ------------------------------------------------------------------
# Project motor list (same 6 motors as the Excel workbook)
# ------------------------------------------------------------------

def build_motor_list() -> List[Motor]:
    return [
        Motor("M-1", "Supply Fan (AHU-1)", "Mechanical Room", 5),
        Motor("M-2", "Return Fan (AHU-1)", "Mechanical Room", 3),
        Motor("M-3", "Chilled Water Pump (P-1)", "Mechanical Room", 20),
        Motor("M-4", "Exhaust Fan (EF-1)", "Roof", 1),
        Motor("M-5", "Cooling Tower Fan (CT-1)", "Roof", 25),
        Motor("M-6", "Air Compressor (AC-1)", "Mechanical Room", 15),
    ]


# ------------------------------------------------------------------
# Report generation
# ------------------------------------------------------------------

def generate_report(motors: List[Motor]) -> List[dict]:
    report = []
    for m in motors:
        fla = m.fla
        awg, _ = select_cable_size(fla)
        breaker = select_breaker_size(fla)
        report.append({
            "Motor ID": m.motor_id,
            "Description": m.description,
            "HP": m.hp,
            "FLA (A)": fla,
            "Min Cable Ampacity (A)": round(fla * 1.25, 2),
            "Cable Size": awg,
            "Max Breaker (A)": round(fla * 2.5, 2),
            "Selected Breaker (A)": breaker,
        })
    return report


def print_report(report: List[dict]) -> None:
    headers = list(report[0].keys())
    widths = [max(len(str(row[h])) for row in report + [dict(zip(headers, headers))]) + 2 for h in headers]

    def fmt_row(values):
        return "".join(str(v).ljust(w) for v, w in zip(values, widths))

    print(fmt_row(headers))
    print("-" * sum(widths))
    for row in report:
        print(fmt_row(row.values()))


def export_csv(report: List[dict], filename: str = "motor_load_report.csv") -> None:
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=report[0].keys())
        writer.writeheader()
        writer.writerows(report)
    print(f"\nExported: {filename}")


# ------------------------------------------------------------------
# Run
# ------------------------------------------------------------------

if __name__ == "__main__":
    motors = build_motor_list()
    report = generate_report(motors)
    print_report(report)
    export_csv(report)
