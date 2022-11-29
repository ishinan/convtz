#!/usr/local/bin/python
"""
Version: 0.4
Feature:
    1. Convert epoch time based on a timezone
    2. Convert a timestamp based on a timezone
    3. List available timezones

Requirements
    - pytz package which is not python built-in 

Change Log:
    - Print the current epoch time when there is no argument
    - Added pick_a_timezone class method so that epoch and ascii time convert use the same way to pick a timezone

Enhancement Plan:
    - As a module, this class should return data, instead of printing data in the class
"""
import sys
import argparse
from datetime import datetime
import re
import calendar

import pytz

class ConvertTimezone:
    @classmethod
    def list_timezones(cls, filter_tz=None):
        '''
        -l option: list all available timezone based on -z option
        default timezone is US
        '''
        if filter_tz is None:
            filter_tz = "US"
        # Not used at this time
        # total_available_zones = len(pytz.all_timezones)
        for zone in pytz.all_timezones:
            if filter_tz in zone:
                    print(zone)

    @classmethod
    def pick_a_timezone(cls, filter_tz=None):
        '''
        Select a timezone
        '''
        picked_tzone='UTC'
        # If filter_tz is not None, 
        #   1. Try to find a timezone and pick the first hit
        #   2. Print the timestamp with the timezone
        if filter_tz:
            for zone in pytz.all_timezones:
                if filter_tz in zone:
                        picked_tzone=zone
                        break
        return picked_tzone

    @classmethod
    def covert_epochtime(cls, e_timestamp=None,e_tz=None):
        '''
        Convert epoch time to a selected timezone timestamp
        '''
        if e_timestamp is None:
            # define epoch, the beginning of times in the UTC timestamp world
            epoch = datetime(1970,1,1,0,0,0)
            now = datetime.utcnow()
            e_timestamp = (now - epoch).total_seconds()
            print("(epoch:{})".format(int(e_timestamp)))

        if e_tz:
            picked_zone = cls.pick_a_timezone(filter_tz=e_tz)
            print('Selected Timezone: {}'.format(picked_zone))
            tz = pytz.timezone(picked_zone)
            dt = datetime.fromtimestamp(e_timestamp , tz)
            print(dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
            print("-------------------------")

        for tzone in [ 'UTC', 'America/New_York', 'US/Pacific']:
            # get time in tz
            tz = pytz.timezone(tzone)
            dt = datetime.fromtimestamp(e_timestamp , tz)
            # print it
            print(dt.strftime('%Y-%m-%d %H:%M:%S %Z%z'))

    @classmethod
    def is_number(cls, data):
        if data == "Zero":
            # This is a hidden option. It is redundant.
            epoch_origin = datetime(1970,1,1,0,0,0)
            now = datetime.utcnow()
            data = (now - epoch_origin).total_seconds()
        data = float(data)
        if isinstance(data, float):
            return data
        else:
            msg = "{} is not integer or floating".format(data)
            raise argparse.ArgumentTypeError(msg)

    @classmethod
    def parse_timeformat(cls, ascii_timestamp, tzone=None):
        '''
        Accept mutiple timestamp formats:
            1) Dec 18, 2018 15:43:52.504364000 => %h %d, %Y %H:%M:%S
            2) 2018-01-01 15:43:52 => %Y-%m-%d %H:%M:%S
            3) 2018-01-01:15:43:52 => %Y-%m-%d:%H:%M:%S
            4) 2018-01-01T15:43:52 => %Y-%m-%dT%H:%M:%S
            5) 2018/01/01 15:43:52 => %Y/%m/%d %H:%M:%S
            6) 01/01/2018 15:43:52 => %m/%d/%Y %H:%M:%S
            7) 02/May/2016:14:59:39 => %d/%h/%Y:%H:%M:%S
        tzone: Time zone (default UTC)
        '''
        list_timeformats = [ 
            (r'^(\w{3}\s\d{2},\s\d{4}\s\d{1,2}:\d{1,2}:\d{1,2})', '%b %d, %Y %H:%M:%S'),
            (r'^(\d{4}-\d{2}-\d{2}\s\d{1,2}:\d{1,2}:\d{1,2})', '%Y-%m-%d %H:%M:%S'),
            (r'^(\d{4}-\d{2}-\d{2}:\d{1,2}:\d{1,2}:\d{1,2})', '%Y-%m-%d:%H:%M:%S'),
            (r'^(\d{4}-\d{2}-\d{2}T\d{1,2}:\d{1,2}:\d{1,2})', '%Y-%m-%dT%H:%M:%S'),
            (r'^(\d{4}/\d{2}/\d{2}\s\d{1,2}:\d{1,2}:\d{1,2})', '%Y/%m/%d %H:%M:%S'),
            (r'^(\d{2}/\d{2}/\d{4}\s\d{1,2}:\d{1,2}:\d{1,2})', '%m/%d/%Y %H:%M:%S'),
            (r'^(\d{2}/\w{3}/\d{4}\s\d{1,2}:\d{1,2}:\d{1,2})', '%d/%b/%Y:%H:%M:%S')
        ] 

        # Find a timeformat to parse the timestamp
        date_time_str = None
        for timeformat_regex, strftime_format in list_timeformats:
            matched_str = re.match(timeformat_regex, ascii_timestamp)
            if matched_str:
                date_time_str = matched_str.group(1)
                strp_TimeFormat = strftime_format
                break
        # If we could not find a timeformat, use epoch time as an example instead of errors
        #   - Maybe we should just show available format and exist?
        if date_time_str is None:
            date_time_str = '1970-01-01 00:00:00' 
            strp_TimeFormat = '%Y-%m-%d %H:%M:%S'
            print("Couldn't parse the timestamp. Showing epoch time zero.")

        picked_tzone = cls.pick_a_timezone(filter_tz=tzone)
        print('Selected Timezone: {}'.format(picked_tzone))
        # Define our timezone
        tz = pytz.timezone(picked_tzone) 
        # Create time_struct object
        dt = datetime.strptime(date_time_str, strp_TimeFormat)
        dt_timezone = tz.localize(dt)

        # This is to build UTC time 
        ts = dt_timezone.astimezone(pytz.utc)
        epoch = int(calendar.timegm(ts.utctimetuple()))

        # Print the timestamp and its epoch time: 
        # - This is based on the timezone provided by user or default UTC
        print("{} (epoch:{})".format(dt_timezone.strftime('%Y-%m-%d %H:%M:%S %Z%z'), epoch))
        print("-------------------------")

        cls.covert_epochtime(float(epoch))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, 
                                     description='Convert epoch time to multiple timezone timestamps')
    #requiredGroup = parser.add_argument_group('Required arguments(one of them)')
    requiredGroup = parser.add_argument_group()
    requiredGroup.add_argument("-e", "--epoch", 
                        required=False,
                        dest="epoch_time", 
                        nargs='?',
                        const="Zero",
                        help="An epoch time to convert. Without value, the current time will be used", 
                        metavar="epoch_time",
                        #default=argparse.SUPPRESS,
                        type=ConvertTimezone.is_number)
    requiredGroup.add_argument("-t", "--timestamp", 
                        required=False,
                        dest="timestamp", 
                        nargs='?',
                        const="Zero",
                        help="A date time string to a timestamp with timezones.", 
                        metavar="timestamp",
                        #default=argparse.SUPPRESS,
                        type=str)
    requiredGroup.add_argument("-l", "--list_timezone", 
                        required=False,
                        dest="ls_timezone", 
                        action="store_true",
                        #default=argparse.SUPPRESS,
                        help="Print available timezone. if -l is on without -z, this lists US timezones. \
                        Use -z option for other tz")
    requiredGroup.add_argument("-z", "--zone", 
                        required=False,
                        dest="filter_timezone", 
                        nargs=1,
                        #default=argparse.SUPPRESS,
                        type=str,
                        help="A string to pick a timezone for -e, -t, or -l  option. Not regex")
    requiredGroup.add_argument("-D", "--DEBUG", 
                        required=False,
                        action="store_true",
                        dest="print_debug", 
                        #default=argparse.SUPPRESS,
                        help="Print parsed arguments")
    requiredGroup.add_argument("-v", "--version", 
                        action='version', 
                        version='%(prog)s 0.4')

    # parse_args() to returns options and positional args 
    args_results = parser.parse_args()

    # Debug option: Not implemented
    if args_results.print_debug:
        print("Parsed Args: {}".format(parser.parse_args()))

    # Check if epock_time is specified
    epoch_timestamp = None
    if isinstance(args_results.epoch_time, float):
        epoch_timestamp =  args_results.epoch_time

    # Check if a timezone is specified
    filter_timezone = None
    if args_results.filter_timezone:
        filter_timezone = args_results.filter_timezone[0] 

    # To list timezones, or process an epoch time or a timestamp
    if args_results.ls_timezone:
        # Option -l
        ConvertTimezone.list_timezones(filter_timezone)
    elif args_results.timestamp:
        # Option -t
        ConvertTimezone.parse_timeformat(args_results.timestamp, filter_timezone)
    else:
        # Option -e or  no options
        ConvertTimezone.covert_epochtime(epoch_timestamp, filter_timezone)

    sys.exit()
