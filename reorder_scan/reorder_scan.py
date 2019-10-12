#!/usr/bin/env python3
"""
Reorder scanned files

If have scanner with feeder but without duplex unit, you need to reorder
your scans if you scan both sides of the same paper stack.
"""

import argparse
import pathlib
import glob
import shutil
import math
import os
import pprint


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
    front = normalize_files(args.files)
    back = normalize_files(args.back)

    if len(back) == 0:
        if len(front) % 2 == 1:
            raise Exception("Something is wrong with the scan, the number of pages should be even")
        back = front[len(front) / 2 :]

    has_duplicates = lambda x: len(x) != len(set(x))

    if has_duplicates(front) or has_duplicates(back):
        raise Exception("Duplicates found")

    new_files = reorder(front, back, os.path.join(args.output_folder, args.output_prefix))

    if args.dry_run:
        pprint.pprint(new_files)
    else:
        for src, dest in new_files.items():
            shutil.copy(src, dest)


def reorder(front, back, out_prefix=""):
    new_order = {}
    back.reverse()
    num_digits = math.ceil(math.log10(len(front) + len(back)))
    file_counter = 0
    format_string = out_prefix + "_{cnt:0" + str(num_digits) + "}{ext}"
    get_file_type = lambda x: x[x.rfind("."):]
    for f,b in zip(front,back):
        new_order[f] = format_string.format(cnt=file_counter, ext=get_file_type(f))
        file_counter += 1
        new_order[b] = format_string.format(cnt=file_counter, ext=get_file_type(b))
        file_counter += 1

    return new_order


def normalize_files(files):
    if type(files) != list:
        raise Exception()
    normalized_files = []
    for idx, fname in enumerate(files):
        fname = str(pathlib.Path(fname).absolute())
        if pathlib.os.path.exists(fname):
            normalized_files.append(fname)
        else:
            # string could be an expression, try to expand it
            possible_files = glob.glob(fname)
            if len(possible_files) > 0:
                for fname_from_glob in possible_files:
                    fname_from_glob = str(pathlib.Path(fname).absolute())
                if pathlib.os.path.exists(fname_from_glob):
                    normalized_files.append(fname_from_glob)
            else:
                raise Exception(f"File {fname} does not exists")

    return normalized_files


if __name__ == "__main__":
    main()
