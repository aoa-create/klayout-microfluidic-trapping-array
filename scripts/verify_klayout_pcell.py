"""Create one Trapping Array PCell instance and write a smoke-test GDS file.

Run with KLayout, for example:
  klayout_app.exe -b -r scripts/verify_klayout_pcell.py -rd output=docs/evidence/v0.0.1-pcell-placement-smoke.gds
"""

import os
import xml.etree.ElementTree as ET

import pya


output_path = globals().get(
    "output", os.path.join(os.getcwd(), "docs", "evidence", "v0.0.1-pcell-placement-smoke.gds")
)
output_path = os.path.abspath(output_path)
os.makedirs(os.path.dirname(output_path), exist_ok=True)
debug_path = os.path.join(os.path.dirname(output_path), "v0.0.1-pcell-smoke.log")


def note(message):
    with open(debug_path, "a", encoding="utf-8") as stream:
        stream.write(message + "\n")


if os.path.exists(debug_path):
    os.remove(debug_path)
note("start")

# Prefer the profile-installed macro and only execute the repository payload if
# KLayout did not auto-register the library for this process.
repository_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
macro_path = os.path.join(repository_root, "trapping_array_pcell.lym")
library = pya.Library.library_by_name("Trapping Array")
if library is None:
    macro_text = ET.parse(macro_path).getroot().find("text").text
    if not macro_text:
        raise RuntimeError("The macro does not contain an executable Python payload")
    exec(compile(macro_text, macro_path, "exec"), {"__file__": macro_path})
    note("repository macro payload executed")
    library = pya.Library.library_by_name("Trapping Array")
else:
    note("profile macro auto-registered library")

if library is None:
    raise RuntimeError("The 'Trapping Array' library is not registered")
note("library registered")

pcell_name = "TrapArray_A — Fixed grid"
pcell_declaration = library.layout().pcell_declaration(pcell_name)
if pcell_declaration is None:
    raise RuntimeError("The TrapArray_A PCell declaration is not registered")
note("PCell declaration registered")

layout = pya.Layout()
top = layout.create_cell("TRAPPING_ARRAY_P_CELL_SMOKE")
pcell_index = layout.add_pcell_variant(library, pcell_declaration.id(), {})
pcell = layout.cell(pcell_index)
if pcell is None or not pcell.is_pcell_variant():
    raise RuntimeError("KLayout could not instantiate the TrapArray_A PCell")
note("PCell instantiated")

top.insert(pya.CellInstArray(pcell.cell_index(), pya.Trans()))
layout.write(output_path)
note("GDS written")

if not os.path.isfile(output_path) or os.path.getsize(output_path) == 0:
    raise RuntimeError("PCell smoke-test GDS was not written")

print("Library=Trapping Array")
print("PCell=" + pcell_name)
print("TopCell=" + top.name)
print("Output=" + output_path)
print("OutputBytes=" + str(os.path.getsize(output_path)))
