# convtz
Convert date time information based on timezone

# Help (-h) output
```text
usage: convtz.py [-h] [-v] [-e [epoch_time]] [-t [timestamp]] [-l]
                 [-z FILTER_TIMEZONE] [-D]

Convert epoch time to multiple timezone timestamps

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

  -e [epoch_time], --epoch [epoch_time]
                        An epoch time to convert. Without value, the current
                        time will be used (default: None)
  -t [timestamp], --timestamp [timestamp]
                        A date time string to a timestamp with timezones.
                        (default: None)
  -l, --list_timezone   Print available timezone. if -l is on without -z, this
                        lists US timezones. Use -z option for other tz
                        (default: False)
  -z FILTER_TIMEZONE, --zone FILTER_TIMEZONE
                        A string to pick a timezone for -e, -t, or -l option.
                        Not regex (default: None)
  -D, --DEBUG           Print parsed arguments (default: False)
```

# Examples
## Example 1: simply run convtz.py
```text
$ python convtz.py
(epoch:1560219220)
2019-06-11 02:13:40 UTC+0000
2019-06-10 22:13:40 EDT-0400
2019-06-10 19:13:40 PDT-0700
```
## Example 2: List(-l) available timezones (default shows only US/*)
```text
$ python convtz.py  -l
US/Alaska
US/Aleutian
US/Arizona
US/Central
US/East-Indiana
US/Eastern
US/Hawaii
US/Indiana-Starke
US/Michigan
US/Mountain
US/Pacific
US/Samoa
```
## Example 2: List(-l) timezones with a fileter(-z) 
```text
$ python convtz.py  -l -z Canada
Canada/Atlantic
Canada/Central
Canada/Eastern
Canada/Mountain
Canada/Newfoundland
Canada/Pacific
Canada/Saskatchewan
Canada/Yukon
```
## Example 3: Date/Time based on a timezone(-z)
```text
$ python convtz.py -t "2019-06-11 02:13:40" -z Asia/Tokyo
Selected Timezone: Asia/Tokyo
2019-06-11 02:13:40 JST+0900 (epoch:1560186820)
-------------------------
2019-06-10 17:13:40 UTC+0000
2019-06-10 13:13:40 EDT-0400
2019-06-10 10:13:40 PDT-0700
```
## Example 4: Date/Time based on an epoch time(-e) with a timezone(-z)
```text
$ python convtz.py -e 1560186820 -z Asia/Tokyo
Selected Timezone: Asia/Tokyo
2019-06-11 02:13:40 JST+0900
-------------------------
2019-06-10 17:13:40 UTC+0000
2019-06-10 13:13:40 EDT-0400
2019-06-10 10:13:40 PDT-0700
```
## Example 5: Date/Time based on an epoch time(-e) without a specific timezone
```text
$ python convtz.py -e 1560186820
2019-06-10 17:13:40 UTC+0000
2019-06-10 13:13:40 EDT-0400
2019-06-10 10:13:40 PDT-0700
```
