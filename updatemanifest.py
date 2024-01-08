#!/usr/bin/env python3
import json
import os
import time
from glob import glob

IGNORED_PATHS = (".github",)


def main():
    old_manifest = json.load(open("manifest.json", "r", encoding="utf-8"))
    manifest = {
        "repo": {
            "maintainers": old_manifest["repo"]["maintainers"],
            "address": "https://github.com/alex-rusakevich/archaelogical",
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
                art_file = art_file.replace(".art", "").replace(
                    f"{module}-{ver_folder}-", ""
                )

                manifest["packages"][module][ver_folder].append(art_file)

    json.dump(
        manifest, open("manifest.json", "w", encoding="utf-8"), separators=(",", ":")
    )

    with open("last_modified.txt", "w", encoding="utf-8") as f:
        f.write(str(time.time()))


if __name__ == "__main__":
    main()
