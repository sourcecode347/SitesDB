# SitesDB 
**Domain Database Builder with CMS Detection**

<img src="https://github.com/sourcecode347/SitesDB/blob/main/SitesDB.png" style="width:100%;height:auto;"/>

Open SitesDB Script with text editor and go to the Settings Sector and set up the ChromeDriver Path and Ensure you have installed Chrome Or Chromium to your System :

    chromedriver_path='Your ChromeDriver Path Here'

To Setup SitesDB Script execute this command :

    pip install -r requirements.txt

To use the SitesDB Script execute this Command :

    python sitesdb.py -h

    python sitesdb.py -c

Tested On Windows 11 

Not Working On Linux

The Python Script SitesDB Crawls Domains Names from the DuckDuckGo search engine, performs CMS Detection and imports them into a SQLite3 database.

Having a large database with Domains helps you export specific Domains (e.g. with CMS WordPress) to perform various Tests with other tools, each Domain has status=none and when exported it gets status=exported so that you don't create the same lists every time, also the export starts from the most recent Inserts.

Large databases with Domains cost money, you don't find them for free, so if you want to perform various Tests with other tools (e.g. SQLBot), then you must have built your databases.

Have a nice day & Happy Hacking :)
