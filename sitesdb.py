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
from colorama import init, Fore, Style
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
global sitesdatabase,crawl,exportfile,restdbbool,exportbool,importbool,importfile,totalbool,cmsbool, \
cmscountbool,cmscountname,cmslistbool,exportcmsbool,exportcmsname,statusexportbool,statusexportfile,statuscountbool,statusvalue,cmsretestbool,cmsretestname, \
executequerybool,executequery,tor,exportlimit
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
cmsretestbool=False
cmsretestname="Unknown"
executequerybool=False
executequery=""
tor=False
exportlimit=9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
importfile="domains.txt"
help = '''
+------------------+--------------------------------------------------------------------------+--------------------+
| Argument         | Info                                                                     | Default            |
+------------------+--------------------------------------------------------------------------+--------------------+
| -h , --help      | Printing Help Of Arguments ( -h )                                        | NULL               |
+------------------+--------------------------------------------------------------------------+--------------------+
| -c , --crawl     | Crawling New Sites to Database ( -c )                                    | False              |
+------------------+--------------------------------------------------------------------------+--------------------+
| -d , --database  | Name of Database to Use ( -d test.db )                                   | sitesdb.db         |
+------------------+--------------------------------------------------------------------------+--------------------+
| -e , --export    | Export Domains to file if status=none and set status=exported            | domains.txt        |
+------------------+--------------------------------------------------------------------------+--------------------+
| --export-limit   | Export Limit Integer ( -e targets.txt --export-limit 50000 )             | Unlimited          |
+------------------+--------------------------------------------------------------------------+--------------------+
| -i , --import    | Import Domains from file to Database ( -i newtargets.txt )               | domains.txt        |
+------------------+--------------------------------------------------------------------------+--------------------+
| -r , --resetdb   | Setting to All Domains status=none   ( -r -d test.db )                   | sitesdb.db         |
+------------------+--------------------------------------------------------------------------+--------------------+
| -t , --total     | Return Domains Count(*) in Database  (-t -d test.db )                    | False              |
+------------------+--------------------------------------------------------------------------+--------------------+
| --cms            | Detect CMS of Domains in Database with value cms=none (-cms )            | False              |
+------------------+--------------------------------------------------------------------------+--------------------+
| --cms-count      | Return Domains of CMS Count(*) ( --cms-count WordPress )                 | Unknown            |
+------------------+--------------------------------------------------------------------------+--------------------+
| --cms-list       | Printing Supported CMS List ( --cms-list )                               | False              |
+------------------+--------------------------------------------------------------------------+--------------------+
| --cms-export     | Export Domains by CMS and set status=exported ( --cms-export WordPress ) | Unknown            |
+------------------+--------------------------------------------------------------------------+--------------------+
| --cms-retest     | Run New CMS Detection Where CMSName ( --cms-retest Unknown )             | cmsdetected        |
+------------------+--------------------------------------------------------------------------+--------------------+
| --status-export  | Setting status=exported From File list ( --status-export list.txt )      | domains.txt        |
+------------------+--------------------------------------------------------------------------+--------------------+
| --status-count   | Return Domains Count(*) by status ( --status-count none )                | none               |
+------------------+--------------------------------------------------------------------------+--------------------+
| --execute-query  | Execute SQL Query to Database ( --execute-query "SELECT * FROM sites" )  | NULL               |
+------------------+--------------------------------------------------------------------------+--------------------+
| --tor            | Enable Tor Crawling if Tor Browser Running  ( --tor )                    | False              |
+------------------+--------------------------------------------------------------------------+--------------------+
| Example Command  | python sitesdb.py -c -d newtargets.db --tor                                                   |
+------------------------------------------------------------------------------------------------------------------+
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
    if sys.argv[arg-1]=="--cms-retest":
        cmsretestname=str(sys.argv[arg])
        cmsretestbool=True
    if sys.argv[arg-1]=="--status-export":
        statusexportfile=str(sys.argv[arg])
        statusexportbool=True
    if sys.argv[arg-1]=="--status-count":
        statusvalue=str(sys.argv[arg])
        statuscountbool=True
    if sys.argv[arg-1]=="--execute-query":
        executequery=str(sys.argv[arg])
        executequerybool=True
    if sys.argv[arg-1]=="--export-limit":
        exportlimit=int(sys.argv[arg])
    if sys.argv[arg-1]=="--tor":
        tor=True
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
    with sqlite3.connect(sitesdatabase) as conn:
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
def exportcmsdb(cmsname):
    with sqlite3.connect(sitesdatabase) as conn:
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        cursor.execute(f"SELECT domain FROM sites WHERE cms = '{cmsname}' AND status='none' ORDER BY id DESC LIMIT 5000")
        return cursor.fetchall()
def retestcmsdb(cmsname):
    with sqlite3.connect(sitesdatabase) as conn:
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        cursor.execute(f"SELECT domain FROM sites WHERE cms = '{cmsname}' AND status='none' ORDER BY id DESC LIMIT 5000")
        return cursor.fetchall()
def exportdomainsbycmsdb(cms):
    with sqlite3.connect(sitesdatabase) as conn:
        conn.row_factory = lambda cursor, row: row[0]
        cursor = conn.cursor()
        cursor.execute("SELECT domain FROM sites WHERE status = 'none' AND cms=? ORDER BY id DESC LIMIT 5000",(cms,))
        return cursor.fetchall()
def execute_query(sql: str, params=None, fetchall=True, print_results=True):
    """
    Examples:
        execute_query("SELECT * FROM sites LIMIT 10")
        execute_query("SELECT COUNT(*) as total FROM sites")
        execute_query("SELECT * FROM sites WHERE cms = ?", ("WordPress",))
    """
    try:
        with sqlite3.connect(sitesdatabase) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            if sql.strip().upper().startswith("SELECT"):
                rows = cursor.fetchall() if fetchall else cursor.fetchone()
                if not rows:
                    print(Fore.YELLOW + "[-] Not Found Results "+ Style.RESET_ALL)
                    return None
                if print_results:
                    print(Fore.CYAN + f"\n[+] Query Results:" + Style.RESET_ALL)
                    print(Fore.CYAN + f"    {sql[:120]}{'...' if len(sql) > 120 else ''}" + Style.RESET_ALL)
                    print("-" * 100)
                    headers = [description[0] for description in cursor.description]
                    print(Fore.WHITE + " | ".join(f"{h:<30}" for h in headers) + Style.RESET_ALL)
                    print("-" * 100)
                    if isinstance(rows, dict):
                        rows = [rows]
                    for row in rows:
                        print(" | ".join(f"{str(row[h]):<30}" for h in headers))
                    print(f"\n{Fore.GREEN}Total: {len(rows)} Rows{Style.RESET_ALL}\n")
                return rows
            # INSERT / UPDATE / DELETE
            else:
                conn.commit()
                affected = cursor.rowcount
                print(Fore.GREEN + f"[✓] Executed Succesfully! {affected} Rows Affected (!)" + Style.RESET_ALL)
                return affected
    except sqlite3.Error as e:
        print(Fore.RED + f"[!] SQLite Error: {e}" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"[!] Unexpected Error: {e}" + Style.RESET_ALL)
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
    ],
    "Webflow": [
        r'webflow.com', r'data-wf-', r'cdn.prod.website-files.com',
        r'meta content="Webflow" name="generator',
        r'<!-- This site was created in Webflow'
    ],
    "Weebly": [
        r'weebly.com', r'weebly-site.com',
        r'meta name="generator" content="Weebly'
    ],
    "TYPO3": [
        r'typo3', r'/typo3temp/', r'/typo3conf/',
        r'TYPO3', r'meta name="generator" content="TYPO3'
    ],
    "Bitrix": [
        r'bitrix', r'/bitrix/', r'BX_',
        r'Bitrix', r'meta name="generator" content="Bitrix'
    ],
    "OpenCart": [
        r'opencart', r'/catalog/view/theme/', r'OpenCart'
    ],
    "BigCommerce": [
        r'bigcommerce.com', r'static.bigcommerce.com',
        r'BigCommerce'
    ],
    "WooCommerce": [
        r'woocommerce', r'/wp-content/plugins/woocommerce/'
    ],
    "Craft_CMS": [
        r'craftcms', r'Craft CMS', r'data-craft'
    ],
    "Umbraco": [
        r'umbraco', r'/umbraco/', r'Umbraco'
    ],
    "Concrete_CMS": [
        r'concrete', r'concrete5', r'Concrete CMS'
    ],
    "HubSpot": [
        r'hubspot', r'hs-scripts.com', r'HubSpot'
    ],
    "GoDaddy": [
        r'godaddysites.com', r'GoDaddy'
    ],
    "Duda": [
        r'duda.co', r'Duda'
    ],
    "Tilda": [
        r'tilda.ws', r'Tilda'
    ],
    "Strapi": [
        r'strapi', r'Strapi'
    ],
    "Contentful": [
        r'contentful', r'Contentful'
    ],
    "Sanity": [
        r'sanity.io', r'Sanity'
    ],
    "Sitecore": [
        r'sitecore', r'Sitecore'
    ],
    "Kentico": [r'kentico', r'Kentico'],
    "Magnolia": [r'magnolia', r'Magnolia CMS'],
    "Liferay": [r'liferay', r'Liferay'],
    "Alfresco": [r'alfresco', r'Alfresco'],
    "Backbone": [r'backbone', r'Backbone.js'],
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
        print(Fore.CYAN + f"🔍 Analyzing: {url}")
        response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
        content = response.text.lower()
        final_url = response.url
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
    # === Tor Proxy Options ===
    if tor==True:
        chrome_options.add_argument('--proxy-server=socks5://127.0.0.1:9150')
    # === Chrome Options ===
    chrome_options.add_argument('--host-resolver-rules="MAP * 0.0.0.0 , EXCLUDE localhost"')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280,800')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # κρύβει το Selenium
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # === Setting ChromeDriver Path ===
    service = ChromeService(executable_path=chromedriver_path)
    # === Open Browser ===
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
        print(Fore.CYAN + f"[+] DB : {sitesdatabase} Has Reseted , {res} Rows Affected")
    if exportbool==True:
        print(Fore.CYAN + f"📤 Starting export of domains with status=none to {exportfile} From DB : {sitesdatabase}")
        filecreator(exportfile)    
        total_exported = 0
        batch_num = 0
        while True:
            if exportlimit<=total_exported:
                break
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
            domains = exportcmsdb('none')
            if not domains:
                print(Fore.YELLOW + f"[!] No more domains with cms=none and status='none' found.")
                break
            for d in domains:
                setcmsdb(d,detect_cms(get_domain(d)))
                setstatusdb(d,'cmsdetected')
        print(Fore.GREEN + f"\n[+] Detecting completed! {total:,} CMS of domains Updated to {sitesdatabase}")
    if cmsretestbool==True:
        print(Fore.CYAN + f"📤 Starting ReDetecting CMS of domains with cms={cmsretestname} and status=none to {sitesdatabase}")   
        total = 0
        batch_num = 0
        while True:
            batch_num += 1
            domains = retestcmsdb(cmsretestname)
            if not domains:
                print(Fore.YELLOW + f"[!] No more domains with cms={cmsretestname} and status='none' found.")
                break
            for d in domains:
                setcmsdb(d,detect_cms(get_domain(d)))
                setstatusdb(d,'cmsdetected')
        print(Fore.GREEN + f"\n[+] Detecting completed! {total:,} CMS={cmsretestname} of domains Updated to {sitesdatabase}")
    if cmscountbool==True:
        print(Fore.CYAN + f"📊 Total domains in DB : {sitesdatabase} with cms={cmscountname} : ", end="")
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites WHERE cms=? ",(cmscountname,))
            total = cursor.fetchone()[0]
            print(Fore.WHITE + f"{total:,}")
    if cmslistbool == True:
        def spacelen(cmsname):
            return 15-len(cmsname)
        maxtotal=0
        print(Fore.CYAN + "📋 Supported CMS Detection List:\n")
        print(Fore.WHITE + "   Available CMS:")
        for cms in CMS_SIGNATURES.keys():
            with sqlite3.connect(sitesdatabase) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM sites WHERE cms=? ",(cms,))
                total = cursor.fetchone()[0]
                maxtotal+=int(total)
                print(Fore.GREEN + f"   • {cms} {' '*spacelen(cms)}: {total}")
            time.sleep(0.1)
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites WHERE cms='Unknown' ")
            total = cursor.fetchone()[0]
            maxtotal+=int(total)
            print(Fore.GREEN + f"   • Unknown {' '*spacelen('Unknown')}: {total}")
        time.sleep(0.1)
        with sqlite3.connect(sitesdatabase) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM sites WHERE cms='none' ")
            total = cursor.fetchone()[0]
            maxtotal+=int(total)
            print(Fore.GREEN + f"   • none {' '*spacelen('none')}: {total}")
        time.sleep(0.1)
        print(Fore.CYAN + f"\nTotal supported CMS: {len(CMS_SIGNATURES) + 2} With Total Domains : {maxtotal}")
    if exportcmsbool==True:
        print(Fore.CYAN + f"📤 Starting export of domains with status=none and cms={exportcmsname} to {exportcmsname+".txt"} From DB : {sitesdatabase}")
        filecreator(exportcmsname+".txt")    
        total_exported = 0
        batch_num = 0
        while True:
            if exportlimit<=total_exported:
                break
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
    if executequerybool==True:
        execute_query(executequery)