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
    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
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
            if entry.is_dir():
                processDirectory(entry.path, db)
            elif entry.is_file():
                processFile(entry.path, db)
    except PermissionError as ex:
        print ("permission error: {0}".format(ex))


def main(baseDirectory: str):
    """
    Set up the database and begin processing files.
    """
    db = DeDupDatabase()
    processDirectory(baseDirectory, db)
 

if __name__ == "__main__":
    """
    Traverse the directory specified.  For each file, generate a hash and store it
    in the database.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="Base Directory to Traverse")
    args = parser.parse_args()
    main(args.directory)
