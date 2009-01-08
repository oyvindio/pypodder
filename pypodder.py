#!/usr/bin/env python
import re
import os
import urllib2
from xml.dom import minidom

def get_feed_feeds():
    # get feed URIs
    conf_file = open("pypodder.conf", "rU")
    feeds = conf_file.readlines()
    
    # strip newline characters from the feed URIs
    newline_regex = re.compile(os.linesep + "$") 

    feeds_stripped = [] 
    for feed in feeds:
        feed = newline_regex.sub("", feed)
        feeds_stripped.append(feed)

    return feeds_stripped 

def parse_feed(feeds):
    file_uris = []

    for feed_uri in feeds:
        feed = urllib2.urlopen(feed_uri)
        xml = minidom.parse(feed)
        enclosures = xml.getElementsByTagName("enclosure")

        for enclosure in enclosures:
            file_uris.append(enclosure.attributes["url"].value)

    return file_uris

feeds = get_feed_feeds()
print feeds

file_uris = parse_feed(feeds)
print file_uris
