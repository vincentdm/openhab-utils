#!/usr/bin/python2.7
# encoding: utf-8
'''
 -- shortdesc

 is a description

It defines classes_and_methods

@author:     vincentdm

@copyright:  2016 Vincent De Maertelaere 

@license:    license

@contact:    vincentdm@gmail.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

from openhab_utils import staticconfig, Database, GraphGenerator
from datetime import datetime, timedelta
from __builtin__ import str

__all__ = []
__version__ = staticconfig.VERSION
__date__ = '2016-05-28'
__updated__ = '2016-06-04'

DEBUG = 1
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2016 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-v", "--verbose", dest="verbose", action="count", help="set verbosity level [default: %(default)s]")
        parser.add_argument("-o", "--output-file", dest="outfile", default="out.png", required = False, help="the filename (including path) where the image will be stored [default: %(default)s]")
        parser.add_argument("-c", "--connection-string", dest="conn", required = True, help="connection string for the database.  E.g. mysql://username:password@localhost/dbname")
        parser.add_argument("-i", "--item", dest="item_list", action="append", required = True, help="item names to include in the graph")
        parser.add_argument("--start", dest="start", required = False, help="Start of the period")
        parser.add_argument("--end", dest="end", required = False, help="End of the period")
        parser.add_argument("--interval", dest="interval", required = False, help="interval")
        parser.add_argument("--days", dest="days", required = False, help="days")
        parser.add_argument("--hours", dest="hours", required = False, help="hours")
        
        parser.add_argument('-V', '--version', action='version', version=program_version_message)

        # Process arguments
        args = parser.parse_args()
        verbose = args.verbose
        
        if verbose > 0:
            print("Verbose mode on")
            
        
        # Get the database
        db = Database(args.conn)
        generator = GraphGenerator(db)
        #generator.Generate(args.items(), period, start, stop, interval)
        #generator.GenerateLastDay(args.item_list,out_file = args.outfile)
        
        
        """
        Parsing the arguments
        """
        date_end = datetime.now()
        date_start = date_end - timedelta(1)
        if  hasattr(args,'end') and args.end is not None :
            date_end = datetime.strptime(args.end,'%Y%m%d %H%M%S')
        
        if hasattr(args, 'start')  and args.start is not None :
            date_start = datetime.strptime(args.start,'%Y%m%d %H%M%S')
        elif hasattr(args, 'days') and args.days is not None:
            date_start = date_end - timedelta(days = int(args.days))
        elif hasattr(args, 'hours') and args.hours is not None:
            date_start = date_end - timedelta(hours = int(args.hours))
        
            
        
        if (args.verbose > 0):
            print "Using period: {} - {}".format(date_start, date_end)
        
        generator.Generate(args.item_list, date_start, date_end, args.outfile)
        
               
        
            
            

        
        return 0
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        #sys.argv.append("-h")
        sys.argv.append("-v")
        
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = '_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())