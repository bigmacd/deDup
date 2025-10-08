import argparse
import os

from deDupDatabase import DeDupDatabase

htmlStart = """
<html>
<head>
<title>Duplicate File Listing</title>
</head>
<body>
  <table>
"""

htmlEnd = """
  </table>
</body>
</html>
"""


def main(doDelete: bool):
    db = DeDupDatabase(False)
    rows = db.getHashGroups()

    count = 0
    rowcolor = "green"
    with open("dedup.html", 'w') as f:
        f.write(htmlStart)
        for md5row in rows:
            matchingResults = db.getByHash(md5row[0])

            resultSet = {}
            for match in matchingResults:
                f.write(f'<tr bgcolor="{rowcolor}"><td>Filename:</td><td>{match[0]}</td><td>Path:</td><td>{match[1]}</td></tr>')
                if match[0] not in resultSet:
                    resultSet[match[0]] = []
                resultSet[match[0]].append(match[1])

            for k, v in resultSet.items():
                if len(v) > 1:

                    if doDelete:
                        for i in range(len(v), 1, -1):
                            index = i - 1
                            fullPath = f"{v[index]}{os.sep}{k}"
                            print(f"deleting: {fullPath}")
                            count += 1
                            if doDelete:
                                os.remove(fullPath)

            if rowcolor == "green":
                rowcolor="white"
            else:
                rowcolor="green"

        f.write(htmlEnd)
        print(f"Total files deleted: {count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--delete", help="Automatically delete duplicates", action="store_true")
    args = parser.parse_args()
    main(args.delete)
