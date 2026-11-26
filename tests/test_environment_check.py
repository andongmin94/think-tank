"""Prerequisite detection must not imply a verified render or mutate a setup."""

import importlib
from importlib import metadata
from pathlib import Path
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
environment = importlib.import_module("environment_check")


def test_missing_package_is_reported(monkeypatch):
    def missing(name):
        raise metadata.PackageNotFoundError(name)
    monkeypatch.setattr(environment.metadata, "version", missing)
    rows = environment._packages()
    assert len(rows) == 5
    assert all(row["status"] == "missing" for row in rows)


def test_every_offered_template_is_bundled_and_verified():
    result = environment.diagnose()
    rows = {row["venue"]: row for row in result["official_templates"]}
    assert set(rows) == {"ieee-software", "ieee-security-privacy", "joss"}
    assert all(row["status"] == "verified" for row in rows.values())
    assert not result["native_export_verified"]


def test_incompatible_and_unusual_versions_remain_visible(monkeypatch):
    versions = {"python-docx": "0.8.11", "pypdfium2": "5.14.1", "Pillow": "13.0.0",
                "pypandoc_binary": "1.17rc1", "pyparsing": "3.2.0"}
    monkeypatch.setattr(environment.metadata, "version", versions.__getitem__)
    rows = {row["name"]: row for row in environment._packages()}
    assert rows["python-docx"]["status"] == "incompatible"
    assert rows["pypdfium2"]["status"] == "detected"
    assert rows["Pillow"]["status"] == "incompatible"
    assert rows["pypandoc_binary"]["status"] == "unverified_version"
    assert rows["pyparsing"]["status"] == "detected"


def test_detected_prerequisites_do_not_certify_native_export(monkeypatch):
    monkeypatch.setattr(environment, "_packages", lambda: [{"name": "example", "status": "detected"}])
    monkeypatch.setattr(environment.sys, "platform", "win32")
    monkeypatch.setattr(environment, "_word_registration", lambda: {"status": "detected"})
    monkeypatch.setattr(environment.shutil, "which", lambda name: "C:/Windows/powershell.exe")
    monkeypatch.setattr(environment, "pandoc_binary", lambda explicit: Path("C:/pandoc.exe"))
    monkeypatch.setattr(environment.subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a, 0, "pandoc 3.8\n", ""))
    monkeypatch.setattr(environment, "official_template", lambda venue: (Path("C:/template.docx"), {"sha256": "a" * 64}))
    result = environment.diagnose()
    assert result["native_export_prerequisites_detected"] is True
    assert result["native_export_verified"] is False


def test_failed_pandoc_probe_produces_a_diagnostic(monkeypatch):
    monkeypatch.setattr(environment, "pandoc_binary", lambda explicit: (_ for _ in ()).throw(ValueError("Unavailable")))
    result = environment.diagnose()
    assert result["pandoc"]["status"] == "missing_or_unusable"
    assert not result["native_export_prerequisites_detected"]


def test_python_version_banner_is_not_pandoc():
    result = environment.diagnose(sys.executable)
    assert result["pandoc"]["status"] == "missing_or_unusable"
    assert not result["native_export_prerequisites_detected"]


def test_existing_pandoc_does_not_require_a_second_provider(monkeypatch):
    monkeypatch.setattr(environment, "_packages", lambda: [{"name": "python-docx", "status": "detected"},
                                                           {"name": "pypandoc_binary", "status": "missing"}])
    monkeypatch.setattr(environment.sys, "platform", "win32")
    monkeypatch.setattr(environment, "_word_registration", lambda: {"status": "detected"})
    monkeypatch.setattr(environment.shutil, "which", lambda name: "C:/Windows/powershell.exe")
    monkeypatch.setattr(environment, "pandoc_binary", lambda explicit: Path("C:/pandoc.exe"))
    monkeypatch.setattr(environment.subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a, 0, "pandoc 3.8\n", ""))
    monkeypatch.setattr(environment, "official_template", lambda venue: (Path("C:/template.docx"), {"sha256": "a" * 64}))
    result = environment.diagnose("C:/pandoc.exe")
    assert result["native_export_prerequisites_detected"]
    assert result["packages"][1]["status"] == "missing"
    assert not result["packages"][1]["required_for_export"]


def test_cli_retains_existing_output(tmp_path):
    folder = tmp_path / "existing"
    folder.mkdir()
    marker = folder / "keep.txt"
    marker.write_text("unchanged", encoding="utf-8")
    script = Path(environment.__file__)
    result = subprocess.run([sys.executable, str(script), "--output-dir", str(folder)], capture_output=True, text=True)
    assert result.returncode == 2
    assert marker.read_text(encoding="utf-8") == "unchanged"
    assert list(folder.iterdir()) == [marker]


def test_windows_bundled_pandoc_suffix_is_resolved(tmp_path, monkeypatch):
    if sys.platform != "win32":
        return
    from types import SimpleNamespace
    converter = importlib.import_module("_publication_convert")
    binary = tmp_path / "pandoc.exe"
    binary.write_bytes(b"test executable placeholder; never run")
    monkeypatch.delenv("PYPANDOC_PANDOC", raising=False)
    monkeypatch.setattr(converter.shutil, "which", lambda name: None)
    monkeypatch.setitem(sys.modules, "pypandoc", SimpleNamespace(get_pandoc_path=lambda: str(binary.with_suffix(""))))
    assert converter.pandoc_binary() == binary.resolve()


def test_macos_word_and_osascript_count_as_native_prerequisites(monkeypatch):
    monkeypatch.setattr(environment, "_packages", lambda: [{"name": "example", "status": "detected"}])
    monkeypatch.setattr(environment.sys, "platform", "darwin")
    monkeypatch.setattr(environment, "_word_registration", lambda: {"status": "detected"})
    monkeypatch.setattr(environment.shutil, "which", lambda name: "/usr/bin/osascript" if name == "osascript" else None)
    monkeypatch.setattr(environment, "pandoc_binary", lambda explicit: Path("/usr/local/bin/pandoc"))
    monkeypatch.setattr(environment.subprocess, "run", lambda *a, **kw: subprocess.CompletedProcess(a, 0, "pandoc 3.8\n", ""))
    monkeypatch.setattr(environment, "official_template", lambda venue: (Path("/t/template.docx"), {"sha256": "a" * 64}))
    result = environment.diagnose()
    assert result["osascript"] == "/usr/bin/osascript" and result["powershell"] is None
    assert result["native_export_prerequisites_detected"] is True
    assert result["native_export_verified"] is False


def test_macos_word_bundle_is_read_without_launching_word(tmp_path, monkeypatch):
    import plistlib
    bundle = tmp_path / "Microsoft Word.app"
    (bundle / "Contents").mkdir(parents=True)
    with (bundle / "Contents" / "Info.plist").open("wb") as stream:
        plistlib.dump({"CFBundleIdentifier": "com.microsoft.Word", "CFBundleShortVersionString": "16.99"}, stream)
    monkeypatch.setattr(environment, "MAC_WORD_APPS", (tmp_path / "missing.app", bundle))
    found = environment._mac_word_installation()
    assert found["status"] == "detected" and found["version"] == "16.99"
    monkeypatch.setattr(environment, "MAC_WORD_APPS", (tmp_path / "missing.app",))
    assert environment._mac_word_installation()["status"] == "missing"
