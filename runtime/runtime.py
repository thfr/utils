#!/usr/bin/env python3
""" Calculate the runtime of the device: uptime - suspended time """

import subprocess
import datetime


def main():
   logind_log = subprocess.check_output(
       "journalctl --since=today _PID=1".split(), universal_newlines=True)
   logind_log = logind_log.splitlines()[1:]

   parsed_log = parse_log(logind_log)

   runtime = get_uptime(parsed_log)
   print(f"Measured runtime: {runtime}")
   print("Uptime: " +
         subprocess.check_output("uptime", universal_newlines=True)[:-1])


def parse_log(log):
   parsed_log = []
   for line in log:
      line_splitted = line.split()
      date = parse_systemd_date(str.join(' ', line_splitted[0:3]))
      message = str.join(' ', line_splitted[5:])
      parsed_log.append((date, message))

   return parsed_log


def get_uptime(uptime_output):
   start_time = uptime_output[0][0]
   end_time = datetime.datetime.now()
   current_runtime = end_time - start_time

   marker_sleep_starts = "Starting Suspend..."
   marker_sleep_stops = "Finished Suspend."
   sleep_ongoing = False
   sleep_time = datetime.timedelta()
   sleep_start = start_time
   for date, message in uptime_output:
      if not (marker_sleep_starts in message or marker_sleep_stops in message):
         continue
      if marker_sleep_stops in message:
         if not sleep_ongoing:
            # log started with device waking up from sleep
            continue
         sleep_time += date - sleep_start
         sleep_ongoing = False
      if marker_sleep_starts in message:
         if sleep_ongoing:
            raise Exception()
         sleep_ongoing = True
         sleep_start = date

   return current_runtime - sleep_time


def parse_systemd_date(date):
   now = datetime.datetime.now()
   parsed_date = datetime.datetime.strptime(date, "%b %d %H:%M:%S").replace(
       year=now.year, tzinfo=now.tzinfo)
   return parsed_date


if __name__ == "__main__":
   main()
