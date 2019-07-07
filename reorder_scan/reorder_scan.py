#!/usr/bin/env python3
"""
Reorder scanned files

If have scanner with feeder but without duplex unit, you need to reorder
your scans if you scan both sides of the same stack.
"""

import argparse
import pathlib
import glob
import shutil
import math
import os


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--output-prefix", default="", help="Prefix for the renamed files"
    )
    parser.add_argument("--output-folder", default="./", help="Output folder")
    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Do not rename, just print what would have been done",
    )
    parser.add_argument("back_begin", help="The file at which the backside scan starts")
    parser.add_argument("files", nargs="*", help="Files to reorder")
    args = parser.parse_args()

    # check files
    files = args.files
    for idx, fname in enumerate(files):
        fname = str(pathlib.Path(fname).absolute())
        files[idx] = fname
        if not pathlib.os.path.exists(fname):
            # string could be an expression, try to expand it
            possible_files = glob.glob(fname)
            if len(possible_files) > 0:
                for f in possible_files:
                    files.insert(idx, f)
            else:
                raise Exception(f"File {fname} does not exists")

    # make sure the back side file is in the stack
    back = os.path.abspath(args.back_begin)
    if not back in files:
        raise Exception("The backside files must be a member of the files argument")

    # sort files
    if not len(files) == set(files):
        print("Duplicates found, removing")
        files = set(files)
    files = sorted(files)

    # rename
    back_begin = files.index(back)
    rename_list = []
    num_digits = math.log10(len(files))
    front_list = files[:back_begin]
    back_list = files[back_begin:]
    back_list.reverse()
    files = front_list + back_list
    for idx, fname in enumerate(files):
        file_type = fname.split(".")[-1]
        new_file = f"{args.output_prefix}{idx}.{file_type}"
        new_file = pathlib.Path(args.output_folder).joinpath(new_file).absolute()
        rename_list.append(new_file)

    for old, new in zip(files, rename_list):
        print(f"Renaming {old} to {new}")
        if not args.dry_run:
            os.rename(old, new)


if __name__ == "__main__":
    main()
