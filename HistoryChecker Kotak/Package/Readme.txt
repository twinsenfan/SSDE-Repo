Format of script
Historychecker SQLServer Username password Day

Replace the days with actual number you want the script to check against DB, it will print out all incidents with status "escalated" to a comma delimited log file "result.csv" in the same folder.

Example, for checking incident in past 20 days
Historychecker 10.239.1.7 Username password 20

You can open the output with excel directly but would suggest you perform a import with the Excel data function with a better looking result.