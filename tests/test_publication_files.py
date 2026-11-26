"""Artifact paths refuse user links but accept the operating system's own."""
import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import _publication_files as files  # noqa: E402


def test_system_temporary_directory_is_accepted():
    # On macOS this path goes through the root-owned /var -> /private/var link.
    with tempfile.TemporaryDirectory() as temporary:
        files.ensure_unlinked(Path(temporary) / "artifact.json")


@pytest.mark.skipif(os.name == "nt", reason="creating symlinks needs extra privileges on Windows")
def test_user_symlink_is_still_refused(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real, target_is_directory=True)
    with pytest.raises(ValueError, match="symlinks or junctions"):
        files.ensure_unlinked(link / "artifact.json")


def test_only_root_owned_top_level_links_are_system_links():
    if os.name == "nt":
        assert not files._system_link(Path("C:/var"), SimpleNamespace(st_uid=0))
        return
    root_owned, user_owned = SimpleNamespace(st_uid=0), SimpleNamespace(st_uid=501)
    assert files._system_link(Path("/var"), root_owned)
    assert not files._system_link(Path("/var"), user_owned)
    assert not files._system_link(Path("/Users/someone/var"), root_owned)
