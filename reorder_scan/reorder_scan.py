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
    parser.add_argument(
        "-b",
        "--back",
        nargs="*",
        help="The file at which the backside scan starts or all backside files",
    )
    parser.add_argument("-f", "--files", nargs="*", help="Files to reorder")
    args = parser.parse_args()

    # check files
    front = args.files
    check_files(front)
    back = args.back
    check_files(back)

    overlap = len(set(front) - set(back))

    if overlap == 0:
        sort_func = mode_1list
    elif overlap == 1:
        sort_func = mode_2lists
    else:
        # TODO error message
        raise Exception()

    rename_list = sort_func(front, back)

    # sort files
    if not len(front) == set(front):
        print("Duplicates found, removing")
        front = set(front)
    front = sorted(front)

    # rename
    back_begin = front.index(back)
    rename_list = []
    num_digits = math.log10(len(front))
    front_list = front[:back_begin]
    back_list = front[back_begin:]
    back_list.reverse()
    front = front_list + back_list
    for idx, fname in enumerate(front):
        file_type = fname.split(".")[-1]
        new_file = f"{args.output_prefix}{idx}.{file_type}"
        new_file = pathlib.Path(args.output_folder).joinpath(new_file).absolute()
        rename_list.append(new_file)

    for old, new in zip(files, rename_list):
        print(f"Renaming {old} to {new}")
        if not args.dry_run:
            os.rename(old, new)


def mode_1list(front, back):
    pass


def mode_2lists(front, back):
    pass


def check_files(files):
    if type(files) != list:
        raise Exception()
    for idx, fname in enumerate(files):
        fname = str(pathlib.Path(fname).absolute())
        front[idx] = fname
        if not pathlib.os.path.exists(fname):
            # string could be an expression, try to expand it
            possible_files = glob.glob(fname)
            if len(possible_files) > 0:
                for f in possible_files:
                    front.insert(idx, f)
            else:
                raise Exception(f"File {fname} does not exists")


if __name__ == "__main__":
    main()
