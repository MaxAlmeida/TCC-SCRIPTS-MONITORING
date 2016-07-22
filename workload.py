import subprocess
import re
import os
import time

def average_time_elapsed(command, times, directory):
  report_file = '/mnt/report_file'
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
      sum_average += float(value[0])*60+float(value[1])
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
  command = "(time sh -c 'bzip2 -c --best file.txt > file.txt.bz') 2>> /mnt/report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command,times,directory)
  print time_score 
  

def run_grep(times):
  command = "(time sh -c  \"grep -aoE '[123]+' random | tr -d '\n'\") 2>> /mnt/report_file" 
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command,times,directory)
  print time_score

def run_povray(times):
  command = "(time sh -c \"povray benchmark.pov\") 2>> /mnt/report_file"
  directory = '/root/povray/povray-3.6/scenes/advanced'
  time_score = average_time_elapsed(command,times,directory)
  print time_score

def run_cp(times):
  command = "(time sh -c \"cp file_cp.txt file_cp_copy.txt\") 2>> /mnt/report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command, times, directory)
  print time_score

def run_crypt(times):
  command = "(time sh -c \"./encrpyt.sh\";\"./decrypt.sh\") 2>> /mnt/report_file"
  directory = '/mnt/TCC-SCRIPTS-MONITORING'
  time_score = average_time_elapsed(command, times, directory)
  print time_score

run_crypt(3)
