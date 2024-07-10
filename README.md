# What is EUROPE?

EUROPE is a program desined to extract data from churchofjesuschrist.org and ysaprofiles.org. This program was designed speicifcally for one user, me, when I was membership clerk of my local congregation. This program relied on hardcoded links and credentials, so in its current state, it will not run, however, I've create a executable called demo.exe which will give you an idea of how the program functioned (it's also a lot faster because it's not actually a webscraper.)

# How to Use EUROPE

Upon running the program, you will be given a set of options:

1) Extract - Scrape membership data from churchofjesuschrist.org and ysaprofiles.org and combine the data into a master list.
2) Update - This feature was never implemented.
3) Report - Display membership information
    1) Ward Status Report - Displays full member list, members with only a church record, members with only a YSA profile, and members with both.
    2) Display Inconsistencies - For each member, information discrepencies between churchofjesuschrist.og and ysaprofiles.org are displayed.
    3) Display Changes - Displays members who have been added/removed since the last extraction.
4) Optimize - Format membership data on website. This may be done for either or both sites.
5) Publish - This feature was never implemented.
6) Edit
   1) Merge - Merge duplicate members.
    
?) Displays information about options
q) Exits program

# Retrospective Observations

When I originally wrote this program, it did not loop.
Sometimes I used the strings "True" and "False" instead of booleans True and False like a psychopath.
There is no error checking in the merge function. This user has to type the merging members' names perfectly or the program will crash.
The discrepency checking does not account for differing states.
There is no functionality to copy data from 43rd Ward Master List.txt to Backup.txt

Why are there so many unresolved bugs? Because I had just learned Python, I knew how to work around the bugs, and the lifespan of this project was not very long. Otherwise, I would have taken more time to fine-tune it.


