# -*- coding: utf-8 -*-

import urllib, urllib2
import sys
import json
import linecache
import datetime
import calendar
import os
import dateutil.parser
import collections
import codecs

class LFMPy:

   def __init__(self, username="robz88", filename="output.txt"):
      self.LFM_URL = "http://ws.audioscrobbler.com/2.0/?"
      self.API_KEY = "4b9024f7f463c51f13960fe5cedebab9"
      self.username = username
      self.filename  = filename


   """
   Craft the last api request using command line arguments and details from file
   """
   def send_request(self, args, **kwargs):
      #load supplied argsuments
      kwargs.update(args)

      #add default args
      kwargs.update({"api_key" : self.API_KEY,
                     "format" : "json"})

      try:
         params = self.LFM_URL + urllib.urlencode(kwargs)
         data = urllib2.urlopen(params)
         response_data = json.load(data)
         data.close()
         return response_data
      except urllib2.HTTPError, e:
         print "HTTP error: %d" % e.code
      except urllib2.URLError, e:
         print "Network error: %s" % e.reason.args[1]

   def get_recent_tracks(self, last_access="0", first_track="0"):
      args = { "method" : "user.getrecenttracks",
               "user" : username,
               "from" : last_access,
               "to" : first_track}
      
      response_data = self.send_request(args)
      """
      Open file append response to start of the file
      """
      output_file = codecs.open(filename, 'w', "utf-8")
          
      for tracks in response_data["recenttracks"]["track"]:
         if tracks.has_key('nowplaying'):
            continue
         output_file.write("{ \n")
         output_file.write("   \"timestamp\": " +
                            str(dateutil.parser.parse(tracks["date"]["#text"])) + "\",\n")
         output_file.write("   \"track_name\": \"" + tracks["name"] + "\",\n")
         output_file.write("   \"artist_name\": \"" + tracks["artist"]["#text"] + "\",\n")
         output_file.write("   \"album_name\": \"" + tracks["album"]["#text"] + "\",\n")
         output_file.write("   \"image\": \"" + tracks["image"][0]["#text"] + "\"\n")
         output_file.write("}, \n")

         
if __name__ == "__main__":
   username = "docmatrix"
   filename = "output.txt"

   """
   Take in the command line parameters
   """
   if(len(sys.argv) != 3):
      print """Program requires 2 command line arguments 
                           arg1 Lastfm username eg. docmatrix 
                           arg2 Filename to store results"""
   else:
      username = sys.argv[1]
      filename = sys.argv[2]


   """
   If the file passed to the script exists, open it, parse json structure,
   check time of last track, convert time to UNIX time stamp format
   """
   if os.path.exists(filename):
           date_line = linecache.getline(filename, 2)
           #last_access = calendar.timegm(date_line)
   else:
      open(filename,'w').close()
      last_access = "0"

   lastfm_request = LFMPy(username,filename)
   lastfm_request.get_recent_tracks()
