import subprocess
import re
import os
import time
import datetime

def write_report_file(average, file_name): 
  directory = '/mnt/reports/'
  report = open(directory+file_name, 'a')
  report.write(average)
  report.close()
 
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
  print '>>>>Run bzip2 test...'
  command = "(time sh -c 'bzip2 -c --best file.txt > file.txt.bz') 2>> /mnt/report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command,times,directory)
  return time_score 
  

def run_grep(times):
  print '>>> Run Grep test ...'
  command = "(time sh -c  \"grep -aoE '[123]+' random | tr -d '\n'\") 2>> /mnt/report_file" 
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command,times,directory)
  return time_score

def run_povray(times):
  print '>>> Run povray test ...'
  command = "(time sh -c \"povray benchmark.pov\") 2>> /mnt/report_file"
  directory = '/root/povray/povray-3.6/scenes/advanced'
  time_score = average_time_elapsed(command,times,directory)
  return time_score

def run_cp(times):
  print '>>> Run cp test ...'
  command = "(time sh -c \"cp file.txt file_copy.txt\") 2>> /mnt/report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command, times, directory)
  return time_score

def run_crypt(times):
  print '>>> Run crypt test ...'
  command = "(time sh -c \"./encrpyt.sh\";\"./decrypt.sh\") 2>> /mnt/report_file"
  directory = '/mnt/TCC-SCRIPTS-MONITORING'
  time_score = average_time_elapsed(command, times, directory)
  return time_score

def run_cat(times):
  print '>>> Run cat test .. '
  command = "(time sh -c \"cat file.txt > file_copy.txt\") 2>> /mnt/report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command, times, directory)
  return time_score

def run_dd(times):
  print '>>> Run dd test ... '
  command = "(time sh -c \"dd if=/dev/zero of=file_copy.txt bs=8k count=500k\") 2>> /mnt/report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command, times, directory)
  return time_score

def run_gzip(times):
  print '>>> Run gzip test ... '
  command = "(time sh -c \"gzip -c --best file.txt > file.txt.bz\") 2>> /mnt/report_file"
  directory = '/root/huge-file'
  time_score = average_time_elapsed(command, times, directory)
  return time_score

def run_bw_mem(times):
  print '>>> Run bw_mem test ... '
  report_file = '/mnt/report_file'
  command = 'bw_mem 790M rdwr 2>> /mnt/report_file'
 
  if os.path.isfile(report_file):
    os.remove(report_file)

  cont = 1
  while cont <= times:
    os.system(command)
    cont+=1

  sum_average = 0
  score_file = open(report_file, 'r')
  for line in score_file:
    value = re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',line)
    sum_average += float(value[1])
  return float(sum_average/float(times))

def run_iozone(times):
  print '>>> Run iozone ...'
  report_file = '/mnt/report_file'
  command = './iozone -a -i 0 -i 1 -i 2 -s 2000000 -r 4086 2 >> /mnt/report_file'
  os.chdir('/root/iozone3_434/src/current')
  
  if os.path.isfile(report_file):
    os.remove(report_file)

  cont = 1
  while cont <= times:
    os.system(command)
    cont+=1
  
  sum_write = 0
  sum_read = 0
  sum_write_random = 0
  sum_read_random = 0
  
  #average[0] -> write , average[1] -> read, average[2] -> write random, average[3] read random
  average = [0, 0, 0, 0]
  cont_times = 1 
  score_file = open(report_file)
  lines = score_file.readlines()
  while cont_times <= times:
    #get only statistic line
    statistic_line = 28*cont_times+(cont_times-1)*3 
    value = re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',lines[statistic_line])
    print value
    sum_write += float(value[2])
    sum_read += float(value[4])
    sum_read_random += float(value[6])
    sum_write_random += float(value[7]) 
    cont_times+=1

  average[0] = float(sum_write/float(times))
  average[1] = float(sum_read/float(times))
  average[2] = float(sum_write_random/float(times))
  average[3] = float(sum_read_random/float(times))
  return average
  
def run_cachebench(times):
  print '>>> Run cachebench ... '
  report_file = '/mnt/report_file'
  command = './cachebench -b -x0 -m24 -d1 -e1 2 >> /mnt/report_file'
  os.chdir('/root/llcbench/cachebench')

  if os.path.isfile(report_file):
    os.remove(report_file)

  cont = 1
  while cont <= times:
    os.system(command)
    cont+=1

  major_allocation_memmory = '16777216'
  sum_average = 0
  score_file = open(report_file, 'r')
  for line in score_file:
    if major_allocation_memmory in line:
      value = re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',line)
      sum_average += float(value[1])

  return float(sum_average/float(times))       


#get actual time
st  = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M')

#file_name = 'inactive_score_'+str(st)
#crypt_score = 'Ccrypt: ' + str(run_crypt(2)) + '\n'
#write_report_file(crypt_score,file_name)

#cp_score = 'Cp: '+str(run_cp(2)) + '\n'
#write_report_file(cp_score,file_name)

#grep_score = 'Grep: '+str(run_grep(2)) + '\n'
#write_report_file(grep_score,file_name)

#bzip2_score = 'Bzip: '+str(run_bzip2(2)) + '\n'
#write_report_file(bzip2_score, file_name)

#povray_score = 'Povray: '+str(run_povray(1)) + '\n'
#write_report_file(povray_score, file_name)

iozone_score = run_iozone(2)
print 'Iozone write sequential: '+str(iozone_score[0])
print 'Iozone read sequential: '+ str(iozone_score[1])
print 'Iozone write_random: '+ str(iozone_score[2])
print 'IOzone read_random: '+ str(iozone_score[3]) 

#run_grep(1000)
