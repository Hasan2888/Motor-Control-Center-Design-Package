# MCC Electrical Design Package — Small Commercial Building

An integrated electrical design project combining Excel, Python, AutoCAD Electrical,
Revit, and Word into one design package for a small commercial building's
motor control center (MCC). Self-directed project, July–August 2026.

**Final deliverable:** `05_Word/MCC_Electrical_Design_Package.pdf`

## Stack
| Tool | Role |
|---|---|
| Excel | Motor load schedule, cable sizing, panel schedule |
| Python | Automates the load/cable/breaker calculations |
| AutoCAD Electrical | MCC power and control schematic |
| Revit | Equipment layout on a floor plan |
| Word | Compiled final design document |

## Engineering references
- NEC Table 430.250 — full-load current, 3-phase motors
- NEC 430.22 — 125% conductor sizing (continuous duty)
- NEC 430.52 — 250% breaker sizing (motor starting protection)

## Folder structure
```
01_Excel/
    MCC_Motor_Load_Schedule.xlsx        Load schedule, cable sizing, panel schedule

02_Python/
    motor_load_automation.py            Automates the Excel sizing logic
    motor_load_report.csv               Script output, cross-checked against Excel

03_AutoCAD_Electrical/
    MCC_Schematic_Final.png             Finalized power + control circuit
    Design_Process/                     Sketch-to-CAD progression
        01_first_sketch_attempt.jpeg
        02_revised_sketch_NEMA_symbols.jpeg
        03_final_hand_sketch.jpeg
        04_first_autocad_draft.jpeg

04_Revit/
    Floorplan_Final.png                 Electrical room equipment layout
    (Editable .rvt model omitted here for file size — available on request)

05_Word/
    MCC_Electrical_Design_Package.docx  Editable source document
    MCC_Electrical_Design_Package.pdf   Final compiled design package
```
