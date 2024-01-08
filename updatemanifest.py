#!/usr/bin/env python3
import datetime
import json
import os
from glob import glob

IGNORED_PATHS = (".github",)


def main():
    old_manifest = json.load(open("manifest.json", "r", encoding="utf-8"))
    manifest = {
        "repo": {
            "maintainers": old_manifest["repo"]["maintainers"],
            "updated_at": str(datetime.datetime.now()),
        },
        "packages": {},
    }

    modules = (p for p in glob("*") if os.path.isdir(p) and p not in IGNORED_PATHS)

    for module in modules:
        manifest["packages"][module] = {}

        for ver_folder in (p for p in glob("*", root_dir=module)):
            manifest["packages"][module][ver_folder] = []
            ver_path = os.path.join(module, ver_folder)

            for art_file in (p for p in glob("*.art", root_dir=ver_path)):
                manifest["packages"][module][ver_folder].append(art_file)

    json.dump(
        manifest, open("manifest.json", "w", encoding="utf-8"), separators=(",", ":")
    )


if __name__ == "__main__":
    main()
