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
## Example 2: List(-l) timezones with a filter(-z) 
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
## Example 3: Print the current time in your local timezone

- Using `grep -P` option with lookbehind: `ls -l  /etc/localtime | grep -oP "(?<=zoneinfo/).+$"` 
- Using `grep -E` option: `ls -l  /etc/localtime | grep -oE "[^/]+$"` 
```
$ ls -l /etc/localtime
lrwxr-xr-x 1 root wheel 45 Sep 28 12:37 /etc/localtime -> /var/db/timezone/zoneinfo/America/Los_Angeles
$ python convtz.py -z $( ls -l  /etc/localtime | grep -oE [^/]+$ )
(epoch:1669770637)
Selected Timezone: America/Los_Angeles
2022-11-29 17:10:37 PST-0800
-------------------------
2022-11-30 01:10:37 UTC+0000
2022-11-29 20:10:37 EST-0500
2022-11-29 17:10:37 PST-0800
```

## Example 4: Date/Time based on a timezone(-z)

```text
$ python convtz.py -t "2019-06-11 02:13:40" -z Asia/Tokyo
Selected Timezone: Asia/Tokyo
2019-06-11 02:13:40 JST+0900 (epoch:1560186820)
-------------------------
2019-06-10 17:13:40 UTC+0000
2019-06-10 13:13:40 EDT-0400
2019-06-10 10:13:40 PDT-0700
```

## Example 5: Date/Time based on an epoch time(-e) with a timezone(-z)

```text
$ python convtz.py -e 1560186820 -z Asia/Tokyo
Selected Timezone: Asia/Tokyo
2019-06-11 02:13:40 JST+0900
-------------------------
2019-06-10 17:13:40 UTC+0000
2019-06-10 13:13:40 EDT-0400
2019-06-10 10:13:40 PDT-0700
```
## Example 6: Date/Time based on an epoch time(-e) without a specific timezone

```text
$ python convtz.py -e 1560186820
2019-06-10 17:13:40 UTC+0000
2019-06-10 13:13:40 EDT-0400
2019-06-10 10:13:40 PDT-0700
```
