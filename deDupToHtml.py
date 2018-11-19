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

db = DeDupDatabase(False)
rows = db.getHashGroups()

rowcolor = "green"
with open("dedup.html", 'w') as f:
    f.write(htmlStart)
    for md5row in rows:
        matchingResults = db.getByHash(md5row[0])
        for match in matchingResults:
            x = bytes(match[0], 'utf-8')
            y = bytes(match[1], 'utf-8')
            #match[0] = match[0].decode('utf-8').encode('cp437').decode('cp1252')
            #match[1] = match[1].decode('utf-8').encode('cp437').decode('cp1252')
            f.write('<tr bgcolor="{0}"><td>{1}/{2}</td></tr>'.format(rowcolor, x, y))

        if rowcolor == "green":
            rowcolor="white"
        else:
            rowcolor="green"
        
    f.write(htmlEnd)