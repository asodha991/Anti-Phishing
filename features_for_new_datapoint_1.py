# -*- coding: utf-8 -*-
"""Features_For_New_DataPoint.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZdKPunAhsDuh2nu27GAlo8MosXTZMXlH

# Import Libraries
"""

# !pip install tldextract

# !pip install whois

# !pip install favicon

import requests
import favicon

import os
import requests
from subprocess import *
from bs4 import BeautifulSoup
import json
import base64

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns

# from google.colab import drive
# drive.mount('/content/drive')

from urllib.parse import urlparse
import xml.etree.ElementTree as ET 
import datetime
from dateutil.relativedelta import relativedelta
import whois

"""# Feature Extraction"""

Normal_url ='http://intego3.info/EXEL/index.php'
phish_url = 'https://www.computerhope.com/issues/ch000254.htm'

"""1. Check IP and Hexa"""

def to_find_having_ip_add(url):
  import string
  index = url.find("://")
  split_url = url[index+3:]
  index = split_url.find("/")
  split_url = split_url[:index]
  split_url = split_url.replace(".", "")
  counter_hex = 0
  for i in split_url:
    if i in string.hexdigits:
      counter_hex +=1

  total_len = len(split_url)
  having_IP_Address = 1
  if counter_hex >= total_len:
    having_IP_Address = -1

  return having_IP_Address

print(to_find_having_ip_add(Normal_url))
print(to_find_having_ip_add(phish_url))

"""2. URL_len"""

def to_find_url_len(url):
  URL_Length = 1
  # print(len(url))
  if len(url)>=75:
    URL_Length = -1
  elif len(url)>=54 and len(url)<=74:
    URL_length = 0
  
  return URL_Length

print(to_find_url_len(Normal_url))
print(to_find_url_len(phish_url))

"""3. Shortened URL extraction"""

def get_complete_URL(shortened_url):
  command_stdout = Popen(['curl', shortened_url], stdout=PIPE).communicate()[0]
  output = command_stdout.decode('utf-8')
  href_index = output.find("href=")
  if href_index == -1:
    href_index = output.find("HREF=")
  splitted_ = output[href_index:].split('"')
  expanded_url = splitted_[1]
  return expanded_url

# #listing shortening services
# shortening_services = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
#                       r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
#                       r"short\.to|BudURL\.com|ping.fm|post.ly|Just.as|bkite.com|snipr.com|fic.kr|loopt.us|" 
#                       r"doiop.com|short.ie|kl.am|wp.me|rubyurl.com|om.ly|to.ly|bit.do|lnkd.in|db.tt|" 
#                       r"qr.ae|adf.ly|goo.gl|bitly.com|cur.lv|tinyurl.com|bit.ly|ity.im|q.gs|" 
#                       r"po.st|bc.vc|t`witthis.com|u.to|j.mp|buzurl.com|cutt.us|u.bb|yourls.org|" 
#                       r"prettylinkpro.com|scrnch.me|filoops.info|vzturl.com|qr.net|1url.com|tweez.me|v.gd|" 
#                       r"link.zip.net"

def check_for_shortened_url(url):
  famous_short_urls = ["bit.ly", "tinyurl.com", "goo.gl","shorte.st", "go2l.ink", 'x.co',"tr.im", "is.gd", "cli.gs",
                       "rebrand.ly", "t.co", "youtu.be","yfrog.com", "migre.me", "ff.im", "tiny.cc", "url4.eu", "twit.ac",
                       "ow.ly", "w.wiki", "is.gd","u.pr", "twurl.nl", "snipurl.comV", "short.to", "BudURL.com",
                       "ping.fm","post.ly","Just.as","bkite.com","snipr.com","fic.kr","loopt.us",
                        "doiop.com","short.ie","kl.am","wp.me","rubyurl.com","om.ly","to.ly","bit.do","lnkd.in","db.tt",
                        "qr.ae","adf.ly","goo.gl","bitly.com","cur.lv","tinyurl.com","bit.ly","ity.im","q.gs",
                        "po.st","bc.vc","t`witthis.com","u.to","j.mp","buzurl.com","cutt.us","u.bb","yourls.org",
                        "prettylinkpro.com","scrnch.me","filoops.info","vzturl.com","qr.net","1url.com","tweez.me","v.gd","link.zip.net"
                       ]

  domain_of_url = url.split("/")[0]
  status = 1
  if domain_of_url in famous_short_urls:
    status = -1

  complete_url = None
  if status == -1:
    complete_url = get_complete_URL(url)

  return (status, complete_url)

check_for_shortened_url(phish_url)

check_for_shortened_url(Normal_url)

"""4. @ in URL"""

def to_find_at(url):
  label = 1
  index = url.find("@")
  if index!=-1:
    label = -1
  
  return label

print(to_find_at(Normal_url))
print(to_find_at(phish_url))

"""5. Redirect"""

def to_find_redirect(url):
  index = url.find("://")
  split_url = url[index+3:]
  label = 1  
  index = split_url.find("//")
  if index!=-1:
    label = -1
  
  return label

print(to_find_redirect(Normal_url))
print(to_find_redirect(phish_url))

"""6. "-" in domain (Prefix_suffix)"""

def to_find_prefix(url):
  index = url.find("://")
  split_url = url[index+3:]
  # print(split_url)
  index = split_url.find("/")
  split_url = split_url[:index]
  # print(split_url)
  label = 1
  index = split_url.find("-")
  # print(index)
  if index!=-1:
    label = -1
  
  return label

print(to_find_prefix(Normal_url))
print(to_find_prefix(phish_url))

"""7. Multi-domains presence"""

def to_find_multi_domains(url):
  url = url.split("://")[1]
  url = url.split("/")[0]
  index = url.find("www.")
  split_url = url
  if index!=-1:
    split_url = url[index+4:]
  index = split_url.rfind(".")
  if index!=-1:
    split_url = split_url[:index]
  counter = 0
  for i in split_url:
    if i==".":
      counter+=1
  
  label = 1
  if counter==2:
    label = 0
  elif counter >=3:
    label = -1
  
  return label

print(to_find_multi_domains(Normal_url))
print(to_find_multi_domains(phish_url))

"""8. Authority"""

def to_find_authority(url):
  index_https = url.find("https://")
  valid_auth = ["GeoTrust", "GoDaddy", "Network Solutions", "Thawte", "Comodo", "Doster" , "VeriSign", "LinkedIn", "Sectigo",
                "Symantec", "DigiCert", "Network Solutions", "RapidSSLonline", "SSL.com", "Entrust Datacard", "Google", "Facebook"]
  
  cmd = "curl -vvI " + url

  stdout= Popen(cmd, shell=True, stderr=PIPE ).communicate()[1]
  std_out = stdout.decode('UTF-8',errors="ignore" )
  index = std_out.find("O=")

  split = std_out[index+2:]
  index_sp = split.find(" ")
  cur = split[:index_sp]
  
  index_sp = cur.find(",")
  if index_sp!=-1:
    cur = cur[:index_sp]
  label = -1
  if cur in valid_auth and index_https!=-1:
    label = 1
  
  return label

print(to_find_authority('https://www.weibull.com/hotwire/issue88/relbasics88.htm'))

print(to_find_authority(Normal_url))
print(to_find_authority(phish_url))

"""9. Domain registration Length"""

import tldextract

def dregisterlen(u):
    extract_res = tldextract.extract(u)
    ul = extract_res.domain + "." + extract_res.suffix
    try:
        wres = whois.whois(u)
        f = wres["Creation Date"][0]
        s = wres["Registry Expiry Date"][0]
        if(s>f+relativedelta(months=+12)):
            return 1
        else:
            return -1
    except:
        return -1

print(dregisterlen(Normal_url))
print(dregisterlen(phish_url))

"""10. Favicon"""

def check_favicon(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain

  favs = favicon.get(url)
  # print(favs)
  match = 0
  for favi in favs:
    url2 = favi.url
    extract_res = tldextract.extract(url2)
    url_ref2 = extract_res.domain

    if url_ref in url_ref2:
      match += 1

  if match >= len(favs)/2:
    return 1
  return -1

url = "https://www.iiitd.ac.in"
check_favicon(url)

"""11. https as part of domain"""

def existenceoftoken(u):
    # Assumption - pagename cannot start with this token
    ix = u.find("//https")
    if(ix==-1):
        return 1
    else:
        return -1

print(existenceoftoken(Normal_url))
print(existenceoftoken(phish_url))

"""## Abnormal Based Features

1. Request URL
"""

def check_request_URL(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain

  command_stdout = Popen(['curl', 'https://api.hackertarget.com/pagelinks/?q=' + url], stdout=PIPE).communicate()[0]
  links = command_stdout.decode('utf-8').split("\n")

  count = 0

  for link in links:
    extract_res = tldextract.extract(link)
    url_ref2 = extract_res.domain

    if url_ref not in url_ref2:
      count += 1

  count /= len(links)

  if count < 0.22:
    return 1
  elif count < 0.61:
    return 0
  else:
    return -1

url = "https://xavier-net.gq/?login=do"

check_request_URL(url)

print(check_request_URL(Normal_url))
print(check_request_URL(phish_url))

"""2. URL of Anchor"""

def check_URL_of_anchor(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain
  html_content = requests.get(url).text
  soup = BeautifulSoup(html_content, "lxml")
  a_tags = soup.find_all('a')

  if len(a_tags) == 0:
    return 1

  invalid = ['#', '#content', '#skip', 'JavaScript::void(0)']
  bad_count = 0
  for t in a_tags:
    link = t['href']

    if link in invalid:
      bad_count += 1

    if url_validator(link):
      extract_res = tldextract.extract(link)
      url_ref2 = extract_res.domain

      if url_ref not in url_ref2:
        bad_count += 1

  bad_count /= len(a_tags)

  if bad_count < 0.31:
    return 1
  elif bad_count <= 0.67:
    return 0
  return -1

def url_validator(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

print(check_URL_of_anchor(Normal_url))
print(check_URL_of_anchor(phish_url))

"""3. Tags"""

def tags(u):
    programhtml = requests.get(u).text
    s = BeautifulSoup(programhtml,"lxml")
    mtags = s.find_all('Meta')
    ud = tldextract.extract(u)
    upage = ud.domain
    mcount = 0
    for i in mtags:
        u1 = i['href']
        currpage = tldextract.extract(u1)
        u1page = currpage.domain
        if currpage not in u1page:
            mcount+=1
    scount = 0
    stags = s.find_all('Script')
    for j in stags:
        u1 = j['href']
        currpage = tldextract.extract(u1)
        u1page = currpage.domain
        if currpage not in u1page:
            scount+=1
    lcount = 0
    ltags = s.find_all('Link')
    for k in ltags:
        u1 = k['href']
        currpage = tldextract.extract(u1)
        u1page = currpage.domain
        if currpage not in u1page:
            lcount+=1
    percmtag = 0
    percstag = 0
    percltag = 0

    if len(mtags) != 0:
      percmtag = (mcount*100)//len(mtags)
    if len(stags) != 0:
      percstag = (scount*100)//len(stags)
    if len(ltags) != 0:
      percltag = (lcount*100)//len(ltags)
      
    if(percmtag+percstag+percltag<17):
        return 1
    elif(percmtag+percstag+percltag<=81):
        return 0
    return -1

print(tags(Normal_url))
print(tags(phish_url))

"""4. SFH"""

def sfh(u):
    programhtml = requests.get(u).text
    s = BeautifulSoup(programhtml,"lxml")
    try:
        f = str(s.form)
        ac = f.find("action")
        if(ac!=-1):
            i1 = f[ac:].find(">")
            u1 = f[ac+8:i1-1]
            if(u1=="" or u1=="about:blank"):
                return -1
            er1 = tldextract.extract(u)
            upage = er1.domain
            erl2 = tldextract.extract(u1)
            usfh = erl2.domain
            if upage in usfh:
                return 1
            return 0
        else:
            # Check this point
            return 1
    except:
        # Check this point
        return 1

print(sfh(Normal_url))
print(sfh(phish_url))

"""5. Submitting to Email"""

def check_submit_to_email(url):
  html_content = requests.get(url).text
  soup = BeautifulSoup(html_content, "lxml")
  # Check if no form tag
  form_opt = str(soup.form)
  idx = form_opt.find("mail()")
  if idx == -1:
    idx = form_opt.find("mailto:")

  if idx == -1:
    return 1
  return -1

print(check_submit_to_email(Normal_url))
print(check_submit_to_email(phish_url))

"""## HTML and JavaScript based Features

1. Redirect
"""

def redirect(url):
  # opt = Popen(["sh", "/red.sh", url], stdout=PIPE).communicate()[0]
  # opt = opt.decode('utf-8')
  # opt = opt.split("\n")

  opt = Popen(["curl", url], stdout=PIPE).communicate()[0]
  # Popen(['curl', shortened_url], stdout=PIPE).communicate()[0] "/red.sh"
  opt = opt.decode('utf-8')
  # print(opt)
  opt = opt.split("\n")

  new = []
  for i in opt:
    i = i.replace("\r", " ")
    new.extend(i.split(" "))
  

  count = 0
  for i in new:
   
    if i.isdigit():
      conv = int(i)
      if conv > 300 and conv<310:
        count += 1

  last_url = None
  for i in new[::-1]:
    if url_validator(i):
      last_url = i
      break

  if (count<=1):
    return 1, last_url
  elif count>=2 and count <4:
    return 0, last_url
  return -1, last_url

ur = "https://bit.ly/segfault"

phish_url2 = "https://oxify.me/tuT2y"

redirect(ur)

print(redirect(Normal_url))
print(redirect(phish_url))

"""2. On mouseover"""

def check_onmouseover(url):
  try:
    html_content = requests.get(url).text
  except:
    return -1
  soup = BeautifulSoup(html_content, "lxml")
  if str(soup).lower().find('onmouseover="window.status') != -1:
    return -1
  return 1

url = "https://google.com"
check_onmouseover(url)

print(check_onmouseover(Normal_url))
print(check_onmouseover(phish_url))

"""3. Rightclick"""

def check_rightclick(url):
  html_content = requests.get(url).text
  soup = BeautifulSoup(html_content, "lxml")
  if str(soup).lower().find("preventdefault()") != -1:
    return -1
  elif str(soup).lower().find("event.button==2") != -1:
    return -1
  elif str(soup).lower().find("event.button == 2") != -1:
    return -1
  return 1

check_rightclick(Normal_url)

check_rightclick(phish_url)

"""4. IFrame"""

def check_iframe(url):
  html_content = requests.get(url).text
  soup = BeautifulSoup(html_content, "lxml")
  if str(soup.iframe).lower().find("frameborder") == -1:
    return 1
  return -1

check_iframe("https://www.google.com")

"""## Domain based Features

1. Age of Domain
"""

url = 'https://xavier-net.gq/?login=do'

def check_age_of_domain(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain + "." + extract_res.suffix
  try:
    whois_res = whois.whois(url)
    if datetime.datetime.now() > whois_res["creation_date"][0] + relativedelta(months=+6):
      return 1
    else:
      return -1
  except:
    return -1

check_age_of_domain(url)

print(check_age_of_domain(Normal_url))
print(check_age_of_domain(phish_url))

"""2. DNS Record"""

# !apt-get install whois

# !pip install python-whois

# !pip install tldextract

def check_dns_record(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain + "." + extract_res.suffix
  try:
    whois_res = whois.whois(url)
    return 1
  except:
    return -1

url = "goiigle.com"
check_dns_record(url)

print(check_dns_record(Normal_url))
print(check_dns_record(phish_url))

"""3. Web traffic"""

def check_web_traffic(url):
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain + "." + extract_res.suffix
  html_content = requests.get("https://www.alexa.com/siteinfo/" + url_ref).text
  soup = BeautifulSoup(html_content, "lxml")
  value = str(soup.find('div', {'class': "rankmini-rank"}))[42:].split("\n")[0].replace(",", "")

  if not value.isdigit():
    return -1

  value = int(value)
  if value < 100000:
    return 1
  return 0

url = "https://hokk-i.com"

check_web_traffic(url)

print(check_web_traffic(Normal_url))
print(check_web_traffic(phish_url))

"""4. PageRank"""

import tldextract
import requests

def get_pagerank(url):
  # pageRankApi = open('/pageRankApi').readline()[:-2]
  extract_res = tldextract.extract(url)
  url_ref = extract_res.domain + "." + extract_res.suffix
  # headers = {'API-OPR': pageRankApi}
  headers = {'API-OPR':'4sgws8wocsc0oskgs4gsoo8gos88sg44gsk4s484'}
  domain = url_ref
  req_url = 'https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D=' + domain
  request = requests.get(req_url, headers=headers)
  result = request.json()
  # print(result)
  value = result['response'][0]['page_rank_decimal']
  if type(value) == str:
    value = 0

  if value < 2:
    return -1
  return 1

get_pagerank("https://linked.in")

print(get_pagerank(Normal_url))
print(get_pagerank(phish_url))

"""5. Statistical Reports"""

import xml.etree.ElementTree as ET

def check_statistical_report(url):
  # # phishTankKey = open('/phishTankKey.txt')
  # # phishTankKey = phishTankKey.readline()[:-1]

  headers = {
        'format': 'json',
        'app_key': '',
        }

  def get_url_with_ip(URI):
      """Returns url with added URI for request"""
      url = "http://checkurl.phishtank.com/checkurl/"
      new_check_bytes = URI.encode()
      base64_bytes = base64.b64encode(new_check_bytes)
      base64_new_check = base64_bytes.decode('ascii')
      url += base64_new_check
      return url

  def send_the_request_to_phish_tank(url, headers):
      """This function sends a request."""
      response = requests.request("POST", url=url, headers=headers)
      return response

  url = get_url_with_ip(url)
  # print(url)
  r = send_the_request_to_phish_tank(url, headers)
  # print(r)
  def parseXML(xmlfile): 

    root = ET.fromstring(xmlfile) 
    verified = False
    for item in root.iter('verified'): 
      if item.text == "true":
        verified = True
        break

    phishing = False
    if verified:
      for item in root.iter('valid'): 
        if item.text == "true":
          phishing = True
          break

    return phishing

  inphTank = parseXML(r.text)
  # print(r.text)

  if inphTank:
    return -1

check_statistical_report("https://www.kaggle.com/akashkr/phishing-url-eda-and-modelling")
check_statistical_report('https://espace-facturation-9c8a01.ingress-erytho.easywp.com/org/customer_center/customer-IDPP00C793/login.php')

Normal_url ='http://intego3.info/EXEL/index.php'
phish_url = 'https://www.computerhope.com/issues/ch000254.htm'

# print(check_statistical_report(Normal_url))
# print(check_statistical_report(phish_url))

"""6. Number of Links Pointing to Page"""

import urllib.request as Ureq
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
def task(url):
    # x=Ureq.urlopen(url)
    # print ("Total Size of the Web Page = ",len(x.read())," Bytes")
    url_p=urlparse(url)
    domain='{uri.scheme}://{uri.netloc}/'.format(uri=url_p)
    # print (domain)
    resp=requests.get(url)
    soup=bs(resp.text,'html.parser')
    r=0
    for link in soup.find_all('a'):
        temp=link.get('href')
        if temp is not None and domain in temp:
          # print(temp)
          r=r+1
        # print(temp)
        # r=r+1
    # print("Total links pointing to same domain = ",r)
    if r > 2:
      return 1
    return -1

Normal_url ='http://intego3.info/EXEL/index.php'
phish_url = 'https://www.computerhope.com/issues/ch000254.htm'

task('https://www.youtube.com/results?search_query=page+rank+implementaton+via+page+rank+API+using+python')
print(task(Normal_url))
print(task(phish_url))

"""5. Google Index"""

def extract_features(url):
  features_extracted = [0]*24
  # phStatus, expanded = check_for_shortened_url(url)
  # features_extracted[2] = phStatus
  # phStatus, last_url = redirect(url)
  # features_extracted[16] = phStatus
  # if expanded is not None:
  #   if len(expanded) >= len(url):
  #     url = expanded

  # if last_url is not None:
  #   if len(last_url) > len(url):
  #     url = last_url
  # print(url)
  features_extracted[0] = to_find_having_ip_add(url)
  features_extracted[1] = to_find_url_len(url)
  phStatus, expanded    = check_for_shortened_url(url)
  features_extracted[2] = phStatus
  features_extracted[3]  = to_find_at(url)
  features_extracted[4] = to_find_redirect(url)
  features_extracted[5] = to_find_prefix(url)
  features_extracted[6] = to_find_multi_domains(url)
  features_extracted[7] = to_find_authority(url)
  features_extracted[8] = dregisterlen(url)
  features_extracted[9] = existenceoftoken(url)
  features_extracted[10] = check_request_URL(url)
  try:
    features_extracted[11] =  check_URL_of_anchor(url)
  except:
    features_extracted[11] = '2' 

  features_extracted[12] = tags(url)
  features_extracted[13] = sfh(url)
  features_extracted[14] = check_submit_to_email(url)
  phStatus, last_url     = redirect(url)
  features_extracted[15] = phStatus
  features_extracted[16] = check_onmouseover(url)
  features_extracted[17] = check_rightclick(url)
  features_extracted[18] = check_age_of_domain(url)
  features_extracted[19] = check_dns_record(url)
  features_extracted[20] = check_web_traffic(url)
  features_extracted[21] = get_pagerank(url)
  features_extracted[22] = task(url)
  features_extracted[23] = check_statistical_report(url)
  

  return features_extracted

def convertEncodingToPositive(data):
  mapping = {-1: 2, 1: 1, 0:0}
  i = 0
  for col in data:
    data[i] = mapping[col]
    i+=1
  return data

import pickle

def predict(url):
  features_extracted = extract_features(url)
  features_extracted = convertEncodingToPositive(features_extracted)
  transformed_point =np.array(features_extracted).reshape(1, -1)
  # model = pickle.load(open("/Ensemble_Model_Nor" , "rb"))
  model = pickle.load(open("Ensemble_Model_Nor", "rb"))
  status = model.predict(transformed_point)
  return status
