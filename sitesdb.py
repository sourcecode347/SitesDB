#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Set ChromeDriver Path
#############################################################################################
### SETTINGS
#############################################################################################
chromedriver_path='D:/0/dev/sb/updater_scripts_win64/chromedriver.exe'
#############################################################################################
### IMPORTS
#############################################################################################
import time,random,os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import sys
from random_word import RandomWords
from termcolor import colored
import colorama
colorama.init()
from colorama import init, Fore
from urllib.parse import urlparse
import sqlite3
import requests
import re
#############################################################################################
### GLOBAL VARIABLES
#############################################################################################
global logo
logo = '''
:'######:'####'########'########:'######:'########:'########::
'##... ##. ##:... ##..::##.....:'##... ##:##.... ##:##.... ##:
 ##:::..:: ##:::: ##::::##:::::::##:::..::##:::: ##:##:::: ##:
. ######:: ##:::: ##::::######::. ######::##:::: ##:########::
:..... ##: ##:::: ##::::##...::::..... ##:##:::: ##:##.... ##:
'##::: ##: ##:::: ##::::##::::::'##::: ##:##:::: ##:##:::: ##:
. ######:'####::: ##::::########. ######::########::########::
:......::....::::..::::........::......::........::........:::
Coded By SourceCode347
'''
print(colored(logo , "green"))
r = RandomWords()
global sitesdatabase,crawl,exportfile,restdbbool,resetdbname,exportbool,importbool,importfile,totalbool,cmsbool, \
cmscountbool,cmscountname,cmslistbool,exportcmsbool,exportcmsname,statusexportbool,statusexportfile,statuscountbool,statusvalue
sitesdatabase="sitesdb.db"
exportfile="domains.txt"
crawl=False
exportbool=False
resetdbbool=False
totalbool=False
importbool=False
cmsbool=False
cmscountbool=False
cmslistbool=False
cmscountname="Uknown"
exportcmsbool="False"
exportcmsname="Unkown"
statusexportbool="False"
statusexportfile="domains.txt"
statuscountbool=False
statusvalue="none"
resetdbname=sitesdatabase
importfile="domains.txt"
help = '''
+------------------+------------------------------------------------------------------+--------------------+
| Argument         | Info                                                             | Default            |
+------------------+------------------------------------------------------------------+--------------------+
| -h , --help      | Printing Help Of Arguments                                       | NULL               |
+------------------+------------------------------------------------------------------+--------------------+
| -c , --crawl     | Crawling New Sites to Database                                   | False              |
+------------------+------------------------------------------------------------------+--------------------+
| -d , --database  | Name of Database to Use                                          | sitesdb.db         |
+------------------+------------------------------------------------------------------+--------------------+
| -e , --export    | Export Domains to file if status=none and set status=exported    | domains.txt        |
+------------------+------------------------------------------------------------------+--------------------+
| -i , --import    | Import Domains from file to Database                             | domains.txt        |
+------------------+------------------------------------------------------------------+--------------------+
| -r , --resetdb   | Setting to All Domains status=none                               | sitesdb.db         |
+------------------+------------------------------------------------------------------+--------------------+
| -t , --total     | Return Domains Count(*) in Database                              | False              |
+------------------+------------------------------------------------------------------+--------------------+
| --cms            | Detect CMS of Domains in Database with value cms=none            | False              |
+------------------+------------------------------------------------------------------+--------------------+
| --cms-count      | Return Domains Count(*) in Database with Specific CMS            | Unknown            |
+------------------+------------------------------------------------------------------+--------------------+
| --cms-list       | Printing Supported CMS List                                      | False              |
+------------------+------------------------------------------------------------------+--------------------+
| --cms-export     | Export Domains by CMS and set status=exported ( CMSName.txt )    | Unknown            |
+------------------+------------------------------------------------------------------+--------------------+
| --status-export  | Setting status=exported From File list                           | domains.txt        |
+------------------+------------------------------------------------------------------+--------------------+
| --status-count   | Return Domains Count(*) in Database with Specific status         | none               |
+------------------+------------------------------------------------------------------+--------------------+
| Example Command  | python sitesdb.py -c -d newtargets.db                                                 |
+----------------------------------------------------------------------------------------------------------+
| Example Command  | python sitesdb.py -e targets.txt                                                      |
+----------------------------------------------------------------------------------------------------------+
| Example Command  | python sitesdb.py -r -d sitesdb.db                                                    |
+----------------------------------------------------------------------------------------------------------+
'''
for arg in range(0,len(sys.argv)):
    if sys.argv[arg-1]=="-d" or sys.argv[arg-1]=="--database":
        sitesdatabase=str(sys.argv[arg])
    if sys.argv[arg-1]=="-p" or sys.argv[arg-1]=="--processes":
        processes=int(sys.argv[arg])
    if sys.argv[arg-1]=="-e" or sys.argv[arg-1]=="--export":
        exportfile=str(sys.argv[arg])
        exportbool=True
    if sys.argv[arg-1]=="-i" or sys.argv[arg-1]=="--import":
        importfile=str(sys.argv[arg])
        importbool=True
    if sys.argv[arg-1]=="-r" or sys.argv[arg-1]=="--reset":
        resetdbbool=True
    if sys.argv[arg-1]=="-c" or sys.argv[arg-1]=="--crawl":
        crawl=True
    if sys.argv[arg-1]=="--cms":
        cmsbool=True
    if sys.argv[arg-1]=="--cms-count":
        cmscountname=str(sys.argv[arg])
        cmscountbool=True
    if sys.argv[arg-1]=="--cms-list":
        cmslistbool=True
    if sys.argv[arg-1]=="--cms-export":
        exportcmsname=str(sys.argv[arg])
        exportcmsbool=True
    if sys.argv[arg-1]=="--status-export":
        statusexportfile=str(sys.argv[arg])
        statusexportbool=True
    if sys.argv[arg-1]=="--status-count":
        statusvalue=str(sys.argv[arg])
        statuscountbool=True
    if sys.argv[arg-1]=="-t" or sys.argv[arg-1]=="--total":
        totalbool=True
    if sys.argv[arg-1]=="-h" or sys.argv[arg-1]=="--help":
        print(Fore.GREEN +f"{help}")
        sys.exit()
if len(sys.argv)==0:
    print(Fore.GREEN +f"{help}")
    sys.exit()
#############################################################################################
### Database Functions
#############################################################################################
def setup_database():
    with sqlite3.connect(sitesdatabase) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sites (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain TEXT,
                status TEXT,
                cms TEXT DEFAULT 'none'
            )
        ''')
        cursor.execute("""
            DELETE FROM sites 
            WHERE domain IS NULL 
               OR domain = '' 
               OR TRIM(domain) = '' 
               OR length(domain) < 3
        """)
        deleted = cursor.rowcount
        conn.commit()
        if deleted > 0:
            print(Fore.RED + f"[!] Deleted {deleted} wrong/empty domains")
def insertdb(domain):
    with sqlite3.connect(sitesdatabase) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM sites WHERE domain = ?", (domain,))
        if cursor.fetchone() is not None:
            return False
        cursor.execute('''
            INSERT INTO sites (domain, status)
            VALUES (?, 'none')
        ''', (domain,))
        conn.commit()
        return True
def resetdb():
    with sqlite3.connect(resetdbname) as conn:
        cursor = conn.cursor() 
        cursor.execute('''
            UPDATE sites 
            SET status = 'none'
        ''')
        rows_affected = cursor.rowcount
        conn.commit()
    return rows_affected
def setstatusdb(domain,status):
    with sqlite3.connect(sitesdatabase) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sites SET status = ? WHERE domain = ?", (status, domain))
        conn.commit()
def setcheckeddb(domain,checked):
    with sqlite3.connect(sitesdatabase) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sites SET checked = ? WHERE domain = ?", (checked, domain))
        conn.commit()
def setcmsdb(domain,cms):
    with sqlite3.connect(sitesdatabase) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE sites SET cms = ? WHERE domain = ?", (cms, domain))
        conn.commit()
def exportdomainsdb():
    with sqlite3.connect(sitesdatabase) as conn:
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        cursor.execute("SELECT domain FROM sites WHERE status = 'none' ORDER BY id DESC LIMIT 5000")
        return cursor.fetchall()
def exportcmsdb():
    with sqlite3.connect(sitesdatabase) as conn:
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        cursor.execute("SELECT domain FROM sites WHERE cms = 'none' ORDER BY id DESC LIMIT 5000")
        return cursor.fetchall()
def exportdomainsbycmsdb(cms):
    with sqlite3.connect(sitesdatabase) as conn:
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        cursor.execute("SELECT domain FROM sites WHERE status = 'none' AND cms=? ORDER BY id DESC LIMIT 5000",(cms,))
        return cursor.fetchall()
#############################################################################################
### CMS Detector
#############################################################################################
# ==================== CMS SIGNATURES ====================
CMS_SIGNATURES = {
    "WordPress": [
        r'/wp-content/', r'/wp-includes/', r'wp-.*\.php',
        r'meta name="generator" content="WordPress',
        r'content="WordPress'
    ],
    "Joomla": [
        r'/administrator/', r'/components/com_',
        r'meta name="generator" content="Joomla!',
        r'Joomla!'
    ],
    "Drupal": [
        r'/sites/default/files/', r'Drupal.settings',
        r'meta name="Generator" content="Drupal',
        r'Drupal'
    ],
    "Shopify": [
        r'cdn.shopify.com', r'Shopify.theme',
        r'checkout.shopify.com'
    ],
    "Magento": [
        r'/skin/frontend/', r'/js/mage/',
        r'meta name="generator" content="Magento'
    ],
    "PrestaShop": [
        r'/img/.*prestashop', r'PrestaShop',
        r'meta name="generator" content="PrestaShop'
    ],
    "Wix": [
        r'wix.com', r'Wix.com'
    ],
    "Squarespace": [
        r'squarespace.com', r'Squarespace'
    ],
    "Ghost": [
        r'ghost-platform', r'Ghost'
    ],
    "Blogger": [
        r'blogspot.com', r'blogger'
    ]
}
def get_domain(url):
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    return url
def detect_cms(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/128.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        content = response.text.lower()
        final_url = response.url
        print(Fore.CYAN + f"🔍 Analyzing: {final_url}")
        print(Fore.CYAN + f"Status Code: {response.status_code}")
        detected = []
        for cms, signatures in CMS_SIGNATURES.items():
            for sig in signatures:
                if re.search(sig.lower(), content):
                    detected.append(cms)
                    break
        if 'wordpress' in content or '/wp-' in content:
            detected.append("WordPress")
        if 'wp-content' in content:
            detected.append("WordPress")
        detected = list(dict.fromkeys(detected))
        if detected:
            print(Fore.GREEN + f"✅ CMS Detected: {', '.join(detected)}")
            return detected[0]
        else:
            print(Fore.YELLOW + "⚠️  Could not detect CMS (Unknown or custom)")
            return "Unknown"
    except requests.exceptions.RequestException as e:
        #print(Fore.RED + f"❌ Connection Error: {e}")
        print(Fore.YELLOW + "⚠️  Could not detect CMS (Unknown or custom)")
        return "Unknown"
    except Exception as e:
        #print(Fore.RED + f"❌ Error: {e}")
        print(Fore.YELLOW + "⚠️  Could not detect CMS (Unknown or custom)")
        return "Unknown"
#############################################################################################
### Functions
#############################################################################################
def domaincleaner(domain):
    if domain.startswith("http://"):
        domain = domain[7:]
    elif domain.startswith("https://"):
        domain = domain[8:]
    if domain.startswith("www."):
        domain = domain[4:]
    return domain.replace("/","")
def filecreator(file_name):
    if not os.path.exists(file_name):
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("")
def rdork():
    rnum = random.randint(0,2)
    if rnum == 0:
        dork = "https://duckduckgo.com/?q="+str(r.get_random_word())+"&t=h_&ia=web"
    elif rnum == 1:
        dork = "https://duckduckgo.com/?q="+str(r.get_random_word()+" "+r.get_random_word())+"&t=h_&ia=web"
    elif rnum == 2:
        dork = "https://duckduckgo.com/?q="+str(r.get_random_word()+" "+r.get_random_word()+" "+r.get_random_word())+"&t=h_&ia=web"
    return dork
def write_domains_to_file(domains, filename):
    if not domains:
        return 0
    with open(filename, "a", encoding="utf-8") as f:
        for domain in domains:
            f.write(domain + "\n")
    return len(domains)
def importdomainsdb():
    if not os.path.exists(importfile):
        print(Fore.RED + f"[!] Import file '{importfile}' not found!")
        return 0
    imported = 0
    skipped = 0
    with open(importfile, "r", encoding="utf-8") as f:
        for line in f:
            domain = line.strip()
            if not domain:
                continue 
            d=domain
            d=urlparse(d).netloc
            if len(str(d).strip().replace(" ",""))==0:
                domain=domaincleaner(domain)
            else:
                domain=domaincleaner(d) 
            if insertdb(domain):
                imported += 1
                if imported % 1000 == 0:
                    print(Fore.CYAN + f"[+] Imported {imported:,} domains so far...")
            else:
                skipped += 1
    return imported, skipped
#############################################################################################
### OPENBROWSER
#############################################################################################
def openbrowser():
    global browser
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280,800')
    chrome_options.add_argument('--log-level=3')
    service = ChromeService(executable_path=chromedriver_path)
    browser = webdriver.Chrome(service=service, options=chrome_options)
    time.sleep(2)
#############################################################################################
### NAVIGATE
#############################################################################################
def navigate(link):
    browser.get(link)
    time.sleep(6)
#############################################################################################
### Main
#############################################################################################
if __name__ == "__main__":
    setup_database()
    if crawl==True:
        print(Fore.CYAN + f"🚀 Sites Crawling Started")
        openbrowser()
        while True:
            navigate(rdork())
            for x in range(0,10):
                try:
                    m=browser.find_element(By.XPATH,"//button[@id='more-results']")
                    m.click()
                    time.sleep(3)
                except:
                    pass
            fl = browser.find_elements(By.XPATH,"//a[@data-testid='result-title-a']")
            for l in fl:
                tl = l.get_attribute("href")
                domain = domaincleaner(urlparse(tl).netloc)
                ins=insertdb(domain)
                if ins==True:
                    print(Fore.CYAN + f"\n[+] Domain : {domain} Inserted to DB : {sitesdatabase}")
                    setcmsdb(domain,detect_cms(get_domain(domain)))
    if resetdbbool==True:
        res=resetdb()
        print(Fore.CYAN + f"[+] DB : {resetdbname} Has Reseted , {res} Rows Affected")
    if exportbool==True:
        print(Fore.CYAN + f"📤 Starting export of domains with status=none to {exportfile}")
        filecreator(exportfile)    
        total_exported = 0
        batch_num = 0
        while True:
            batch_num += 1
            domains = exportdomainsdb()
            if not domains:
                print(Fore.YELLOW + f"[!] No more domains with status=none found.")
                break
            exported = write_domains_to_file(domains, exportfile)
            total_exported += exported
            with sqlite3.connect(sitesdatabase) as conn:
                cursor = conn.cursor()
                cursor.executemany("UPDATE sites SET status = 'exported' WHERE domain = ?", 
                                 [(d,) for d in domains])
                conn.commit()
            print(Fore.GREEN + f"[+] Batch {batch_num}: Exported {exported} domains | Total: {total_exported:,}")
            time.sleep(0.5)
        print(Fore.GREEN + f"\n[+] Export completed! {total_exported:,} domains saved to {exportfile}")
    if importbool==True:
        print(Fore.CYAN + f"📥 Starting import from {importfile} to DB : {sitesdatabase}")       
        imported, skipped = importdomainsdb()
        print(Fore.GREEN + f"[+] Import completed!")
        print(Fore.GREEN + f"✅ Imported : {imported:,} new domains")
        print(Fore.YELLOW + f"⏭  Skipped  : {skipped:,} duplicates")
        print(Fore.CYAN + f"📊 Total domains in DB now: ", end="")
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites")
            total = cursor.fetchone()[0]
            print(Fore.WHITE + f"{total:,}")
    if totalbool==True:
        print(Fore.CYAN + f"📊 Total domains in DB : {sitesdatabase} : now: ", end="")
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites")
            total = cursor.fetchone()[0]
            print(Fore.WHITE + f"{total:,}")
    if cmsbool==True:
        print(Fore.CYAN + f"📤 Starting Detecting CMS of domains with cms=none to {sitesdatabase}")   
        total = 0
        batch_num = 0
        while True:
            batch_num += 1
            domains = exportcmsdb()
            if not domains:
                print(Fore.YELLOW + f"[!] No more domains with cms=none found.")
                break
            for d in domains:
                setcmsdb(d,detect_cms(get_domain(d)))
        print(Fore.GREEN + f"\n[+] Detecting completed! {total:,} CMS of domains Updated to {sitesdatabase}")
    if cmscountbool==True:
        print(Fore.CYAN + f"📊 Total domains in DB : {sitesdatabase} with cms={cmscountname} : ", end="")
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites WHERE cms=? ",(cmscountname,))
            total = cursor.fetchone()[0]
            print(Fore.WHITE + f"{total:,}")
    if cmslistbool == True:
        maxtotal=0
        print(Fore.CYAN + "📋 Supported CMS Detection List:\n")
        print(Fore.WHITE + "   Available CMS:")
        for cms in CMS_SIGNATURES.keys():
            with sqlite3.connect(sitesdatabase) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sites WHERE cms=? ",(cms,))
                total = cursor.fetchone()[0]
                maxtotal+=int(total)
                print(Fore.GREEN + f"   • {cms} : {total}")
            time.sleep(0.1)
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites WHERE cms='Unknown' ")
            total = cursor.fetchone()[0]
            maxtotal+=int(total)
            print(Fore.GREEN + f"   • Unknown : {total}")
        time.sleep(0.1)
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites WHERE cms='none' ")
            total = cursor.fetchone()[0]
            maxtotal+=int(total)
            print(Fore.GREEN + f"   • none : {total}")
        time.sleep(0.1)
        print(Fore.CYAN + f"\nTotal supported CMS: {len(CMS_SIGNATURES) + 2} With Total Domains : {maxtotal}")
    if exportcmsbool==True:
        print(Fore.CYAN + f"📤 Starting export of domains with status=none and cms={exportcmsname} to {exportcmsname+".txt"}")
        filecreator(exportcmsname+".txt")    
        total_exported = 0
        batch_num = 0
        while True:
            batch_num += 1
            domains = exportdomainsbycmsdb(exportcmsname)
            if not domains:
                print(Fore.YELLOW + f"[!] No more domains with status=none and cms={exportcmsname} found.")
                break
            exported = write_domains_to_file(domains, exportcmsname+".txt")
            total_exported += exported
            with sqlite3.connect(sitesdatabase) as conn:
                cursor = conn.cursor()
                cursor.executemany("UPDATE sites SET status = 'exported' WHERE domain = ?", 
                                 [(d,) for d in domains])
                conn.commit()
            print(Fore.GREEN + f"[+] Batch {batch_num}: Exported {exported} domains | Total: {total_exported:,}")
            time.sleep(0.5)
        print(Fore.GREEN + f"\n[+] Export completed! {total_exported:,} domains saved to {exportcmsname+".txt"}")
    if statusexportbool==True:
        print(Fore.CYAN + f"📤 Starting set status=exported of domains list file : {statusexportfile}")
        try:
            with open(statusexportfile, "r", encoding="utf-8") as f:
                domains = [line.strip() for line in f if line.strip() and not line.startswith("#")]
            print(Fore.GREEN + f"[+] Loaded {len(domains):,} domains from {statusexportfile}")
            with sqlite3.connect(sitesdatabase) as conn:
                cursor = conn.cursor()
                cursor.executemany("UPDATE sites SET status = 'exported' WHERE domain = ?", 
                                 [(d,) for d in domains])
                conn.commit()
            print(Fore.GREEN + f"[+] Setted status=exported to Total Domains: {len(domains):,}")
        except FileNotFoundError:
            print(Fore.RED + f"[!] File not found: {statusexportfile}")
            sys.exit(1)
    if statuscountbool==True:
        print(Fore.CYAN + f"📊 Total domains in DB : {sitesdatabase} with status={statusvalue} : ", end="")
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites WHERE status=? ",(statusvalue,))
            total = cursor.fetchone()[0]
            print(Fore.WHITE + f"{total:,}")