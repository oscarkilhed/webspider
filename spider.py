import requests
from pyquery import PyQuery as pq
import inspect
from urlparse import urlparse
from collections import deque
import re


def getUrls(currenturl):
  try:
    r = requests.get(currenturl)
  except requests.exceptions.TooManyRedirects:
    print "Too many redirects on " + currenturl + " skipping"
    return []
  
  html = pq(r.content)
  urls = []

  for a in html("a"):
    href = pq(a).attr("href")
    if href is None or href.startswith("javascript"):
      continue
    if href.startswith("/"):
      urls.append(getRoot(currenturl, href))
    elif re.search("://",href):
      urls.append(href)
    elif href != "#":
      urls.append(getRelative(currenturl, href))
  return urls


def getRoot(currenturl, href):
  parse = urlparse(currenturl)
  return parse.scheme + "://" + parse.netloc + href

def getRelative(currenturl, href):
 return currenturl[0:currenturl.rfind("/")] + "/" + href

urlcollection = {}
queue = deque(["http://www.dn.se/"])

while len(queue) > 0:
  currentlink = queue.popleft()
  
  if urlparse(currentlink).netloc != "www.dn.se":
    continue 

  linksonpage = getUrls(currentlink)

  for link in linksonpage:
    if not link in urlcollection.keys() and not link in queue and not link == currentlink:
      queue.append(link)
  urlcollection[currentlink] = linksonpage
  print currentlink

assert getRoot("http://www.bytbil.com/bilar/", "/test") == "http://www.bytbil.com/test"
assert getRelative("http://www.bytbil.com/bilar/asd", "test/test") == "http://www.bytbil.com/bilar/test/test"
