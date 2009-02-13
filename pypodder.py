#!/usr/bin/env python

import re
import os
import urllib2
import urllib
from xml.dom import minidom

CONFIG_FILE = "pypodder.conf"
LOG_FILE = "pypodder.log"
DEST_DIR = os.environ['HOME']  + os.sep + "tmp/"
LIMIT_DOWNLOADS_PER_FEED = True
MAX_DOWNLOADS_PER_FEED = 5

def strip_newlines(file):
    """Strips newline characters from the end of lines in a file. Returns a list
    of strings containing each line in the file - stripped of newlines - as
    elements."""
    newline_regex = re.compile(os.linesep + "$")
    
    strings = [] 
    for line in file:
        string = newline_regex.sub("", line)
        strings.append(string)

    return strings

# Download each file in file_uris
def download_files(file_uris):
    """Downloads files stored at URIs contained in a list of strings passed as
    input to the function."""

    log_file = open(LOG_FILE, "r+")
    downloaded_podcasts = strip_newlines(log_file)

    downloaded_files = 0
    for uri in file_uris:
        # if the current file URI exists in the log, this file has already been
        # downloaded, and is thus skipped
        if uri in downloaded_podcasts:
            continue
        # if LIMIT_DOWNLOADS_PER_FEED is set, and we have downloaded more files
        # from this feed than MAX_DOWNLOADS_PER_FEED, skip the rest of the
        # files.
        if LIMIT_DOWNLOADS_PER_FEED:
            if downloaded_files >= MAX_DOWNLOADS_PER_FEED:
                break

        # extract filename from the URI 
        uri_split = re.split("/", uri)
        filename = uri_split[len(uri_split) - 1]
        
        # download the file
        urllib.urlretrieve(uri, dest_dir + os.sep + filename)
        log_file.write(uri + os.linesep)
        print "downloading " + uri

        downloaded_files++

def parse_feed(uri):
    """Parses the XML from each feed, looking for tags that look like 
    <enclosure url="something"> in the XML, from which we extract the url 
    attribute, which in turn should contain URIs that should point to 
    podcast media files."""

    print "parsing " + uri

    feed = urllib2.urlopen(uri)
    xml = minidom.parse(feed)
    
    # look for <enclosure> tags
    enclosures = xml.getElementsByTagName("enclosure")

    # extract the url attribute from any <enclosure> tags found
    file_uris = []
    for enclosure in enclosures:
        file_uris.append(enclosure.attributes["url"].value)

    download_files(file_uris)

# Parse config file to get feed URIs
feed_uris = strip_newlines(open(CONFIG_FILE, "rU"))

# Handle each feed URI
for uri in feed_uris:
    parse_feed(uri)
    
# vim: sw=4 sts=4 ts=4 tw=80 
