### File De-Duplication Detection

The program will traverse a directory.  For each file it encounters, it will calculate the file's hash,
then store that information in a database (sqlite3).

Then we can iterate over the entries in the database and find all the duplicates.  

This software was born out of the need to preserve some hard disk space on the home NAS.  My kids would put media
files all over the place, and it was running out of space.

#### deDupDatabase.py

The class that encapsulates all the database operations.

#### deDupGenerator.py

The code that iterates over the files and diretories to generate the hash and create the database entries.

#### deDupToHtml.py

Finds the duplicates and writes out a pretty html file.