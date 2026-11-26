"""Turn pytest JUnit failures into GitHub Actions error annotations.

Annotations are visible on the run summary and through the public check-runs
API, so a failure on one platform can be diagnosed without downloading logs.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def escape(text: str) -> str:
    return text.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def main(report: str) -> int:
    path = Path(report)
    if not path.is_file():
        print(f"::error::pytest did not produce {report}")
        return 0
    root = ET.parse(path).getroot()
    count = 0
    for case in root.iter("testcase"):
        for problem in list(case.findall("failure")) + list(case.findall("error")):
            name = f"{case.get('classname', '')}::{case.get('name', '')}"
            detail = (problem.text or problem.get("message") or "").strip().splitlines()
            # Keep the start (assertion and diff summary) and the end (location).
            tail = "\n".join(detail if len(detail) <= 40 else [*detail[:25], "...", *detail[-12:]])
            source = case.get("file") or case.get("classname", "").replace(".", "/") + ".py"
            line = case.get("line")
            location = f"file={source}" + (f",line={int(line) + 1}" if line else "")
            print(f"::error {location},title={escape(name)[:200]}::{escape(tail)[:4000]}")
            count += 1
            if count >= 40:
                return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1]))
