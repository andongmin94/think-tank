"""Small file operations shared by the skill's document tools."""

import hashlib
import os
from pathlib import Path
import stat


def _system_link(part: Path, metadata: os.stat_result) -> bool:
    """Root-owned links directly under '/', such as macOS /var -> /private/var.

    Only the superuser can create or retarget them, so traversing them cannot
    redirect an artifact. User-created links anywhere else are still refused.
    """
    return os.name != "nt" and part.parent == Path(part.anchor) and metadata.st_uid == 0


def ensure_unlinked(path: Path) -> None:
    """Reject symlinks and Windows junctions before resolving a path."""
    for part in (path.absolute(), *path.absolute().parents):
        try:
            metadata = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(metadata.st_mode) and _system_link(part, metadata):
            continue
        if (stat.S_ISLNK(metadata.st_mode) or
                getattr(metadata, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)):
            raise ValueError("Artifact paths must not traverse symlinks or junctions")


def digest_file(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()
