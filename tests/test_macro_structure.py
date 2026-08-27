from pathlib import Path
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
MACRO = ROOT / "trapping_array_pcell.lym"


def _macro_root() -> ET.Element:
    assert MACRO.is_file(), "trapping_array_pcell.lym must remain at repository root"
    return ET.parse(MACRO).getroot()


def _macro_text() -> str:
    text = _macro_root().findtext("text")
    assert text, "KLayout macro must contain executable Python text"
    return text


def test_macro_metadata_is_explicit() -> None:
    root = _macro_root()
    assert root.tag == "klayout-macro"
    assert root.findtext("version") == "1.0.0"
    assert root.findtext("interpreter") == "python"
    assert root.findtext("autorun") == "true"


def test_expected_pcells_and_embedded_modules_are_present() -> None:
    text = _macro_text()
    expected_tokens = (
        "TrapArray_A",
        "TrapArray_B",
        "core/__init__.py",
        "core/grid.py",
        "core/builder.py",
        "core/primitives.py",
        "core/io_shapes.py",
        "trapping_array_lib.py",
    )
    for token in expected_tokens:
        assert token in text, f"missing expected macro component: {token}"


def test_macro_has_no_network_or_shell_execution_primitives() -> None:
    text = _macro_text()
    forbidden_tokens = (
        "subprocess.",
        "os.system(",
        "requests.",
        "urllib.request",
        "socket.",
    )
    for token in forbidden_tokens:
        assert token not in text, f"unexpected executable capability in macro: {token}"
