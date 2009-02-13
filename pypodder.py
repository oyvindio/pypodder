#!/usr/bin/env python

import re
import os
import urllib2
import urllib
from xml.dom import minidom

###############################################################################
# pypodder - A (very) simple podcatcher.
###############################################################################
# Usage:
#
# Add the URIs of the podcast feeds you want to subscribe to to CONFIG_FILE, 
# one per line. Then run this script to parse the feeds and download podcast 
# media files.
# 
###############################################################################
# Configuration
###############################################################################
#
# The file from which to read feed URIs. URIs should be separated by a newline
# character.
# NOTE: THIS FILE (OBVIOUSLY) NEEDS TO EXIST
CONFIG_FILE = "pypodder.conf"
#
# The file in which a list of downloaded podcasts is maintained - to avoid
# re-downloading files. This is simply a list of URIs to the files that have
# already been downloaded, separated by newline characters.
# NOTE: THIS FILE (NOT AS OBVIOUSLY, BUT STILL) NEEDS TO EXIST
LOG_FILE = "pypodder.log"
#
# The directory in which to save downloaded podcasts. Change this to your
# preference.
DEST_DIR = os.environ['HOME']  + os.sep + "tmp/"
#
# If set to True, the script prints some status output to stdout when running.
# If set to False, output is omitted.
OUTPUT = True
# If LIMIT_DOWNLOADS_PER_FEED is set to True, a maximum of
# MAX_DOWNLOADS_PER_FEED files will be downloaded per feed. To disable this
# functionality, simply set it to False.
# The rationale behind this functionality is to avoid downloading the entire
# back catalogue of a podcast whose feed you have just added. Again, if this is
# what you want, disable it.
LIMIT_DOWNLOADS_PER_FEED = True
#
# The maximum number of files to download per feed if LIMIT_DOWNLOADS_PER_FEED
# is set to True.
MAX_DOWNLOADS_PER_FEED = 5
#
###############################################################################
# Note:
# This script was intended to be a quick reimplementation of Linc's excellent
# bashpodder ( http://lincgeek.org/bashpodder/ ), only entirely in python, and
# with a few modifications that I've added to bashpodder as I've been using it.
#
# Feel free to modify this script to suit your own needs.
###############################################################################


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

    print downloaded_podcasts
    downloaded_files = 0
    for uri in file_uris:
        # if the current file URI exists in the log, this file has already been
        # downloaded, and is thus skipped
        print uri

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
        if OUTPUT:
            print "downloading " + uri
#        urllib.urlretrieve(uri, DEST_DIR + os.sep + filename)
#        log_file.write(uri + os.linesep)

        downloaded_files += 1

def parse_feed(uri):
    """Parses the XML from each feed, looking for tags that look like 
    <enclosure url="something"> in the XML, from which we extract the url 
    attribute, which in turn should contain URIs that should point to 
    podcast media files."""

    if OUTPUT:
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
