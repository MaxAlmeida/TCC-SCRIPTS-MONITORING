import subprocess
import re
import os
import time

def average_time_elapsed(command, times, directory):
  report_file = 'report_file'
  os.chdir(directory)
 
  if os.path.isfile(report_file):
    os.remove(report_file)
 
  cont = 1
  while cont <= times:
    os.system(command)
    cont+=1
 
  #calculate average
  sum_average = 0
  score_file = open(report_file, 'r')
  for line in score_file:
    if "real" in line:
      value = re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',line)
      sum_average += float(value[1])
  return float(sum_average/float(times))


def run_add_double(times):
  report_file = 'suite9.ss'
  os.chdir('/root/aimbench/caldera/suite9')
  # delete previous report 
  if os.path.isfile(report_file):
    os.remove(report_file)
  
  cont = 1
  while cont <= times:
    #run add_double by 30 sec
    os.system("./singleuser <<<$'foreground\n\n3\n/mnt\n'")
    cont+=1

  #calculate average
  sum_average = 0 
  score_file = open(report_file, 'r')
  for line in score_file:
    if "add_double" in line:
      value = re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',line)
      sum_average += int(value[0])
  print float(sum_average)/float(times) 
 
def run_bzip2(times):
  command = "(time sh -c 'bzip2 -c --best file.txt > file.txt.bz') 2>> report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command,times,directory)
  print time_score 
 
run_bzip2(4) 

#def run_grep(times):
  

