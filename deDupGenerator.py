import os
import argparse
import sqlite3
import hashlib
from deDupDatabase import DeDupDatabase



def generateMD5(file: str):
    """
    Generate the hash for this file.
    """
    hash_md5 = hashlib.md5()
    # Use a larger chunk size to reduce syscalls while keeping memory modest
    chunk_size = 1024 * 1024
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def processFile(file: str, db: DeDupDatabase):
    """
    Generate the checksum and store in the database.
    """
    md5 = generateMD5(file)
    parts = os.path.split(file)
    db.insert(parts[0], parts[1], md5)


def processDirectory(directory: str, db: DeDupDatabase):
    """
    Starting in the directory specified, process all the files.
    If you run across a directory, recurse back here.
    """
    try:
        for entry in os.scandir(directory):
            # Skip symlinks to avoid cycles and redundant hashing
            if entry.is_symlink():
                continue
            if entry.is_dir(follow_symlinks=False):
                processDirectory(entry.path, db)
            elif entry.is_file(follow_symlinks=False):
                try:
                    print(f"Processing file: {entry.path}")
                    processFile(entry.path, db)
                except (PermissionError, OSError) as ex:
                    print("file error: {0}".format(ex))
    except PermissionError as ex:
        print ("permission error: {0}".format(ex))


def main(baseDirectory: str):
    """
    Set up the database and begin processing files.
    """
    db = DeDupDatabase()
    # Wrap the entire run in a single transaction for much faster inserts
    db.begin()
    try:
        processDirectory(baseDirectory, db)
    finally:
        db.commit()


if __name__ == "__main__":
    """
    Traverse the directory specified.  For each file, generate a hash and store it
    in the database.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Base Directory to Traverse")
    args = parser.parse_args()
    main(args.directory)
