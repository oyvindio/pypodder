#!/usr/bin/env python
import re
import os
import urllib2
from xml.dom import minidom

def get_feed_uris():
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

def get_file_uris(feeds):
    file_uris = []

    # parse feed xml
    for uri in feeds:
        feed = urllib2.urlopen(uri)
        xml = minidom.parse(feed)
        
        # look for <enclosure> tags
        enclosures = xml.getElementsByTagName("enclosure")

        # extract urls from any enclosure tags found
        for enclosure in enclosures:
            file_uris.append(enclosure.attributes["url"].value)

    return file_uris

def download_files(files):
    for uri in files:
        # extract filename from the URI 
        uri_split = re.split("/", uri)
        filename = uri_split[len(uri_split) - 1]
        
        # download the file
        #urllib.urlretrieve(uri, filename)
        print "dl " + uri + " to " + filename


feeds = get_feed_uris()
#print feeds

file_uris = get_file_uris(feeds)
#print file_uris

download_files(file_uris)
