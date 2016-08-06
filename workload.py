import subprocess
import re
import os
import time
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

def send_email(message,password):
 fromaddr = "darkamui100@gmail.com"
 toaddr = "llewxam150@gmail.com"
 msg = MIMEMultipart()
 msg['From'] = fromaddr
 msg['To'] = toaddr
 msg['Subject'] = "TCC-SCRIPTS-MONITORING"
  
 body = message
 msg.attach(MIMEText(body, 'plain'))
 
 server = smtplib.SMTP('smtp.gmail.com', 587)
 server.starttls()
 server.login(fromaddr, password)
 text = msg.as_string()
 server.sendmail(fromaddr, toaddr, text)
 server.quit()
 

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
    #run add_double by 10 sec
    os.system("./singleuser <<<$'foreground\n\n30\n/mnt\n'")
    cont+=1

  #calculate average
  sum_average = 0 
  score_file = open(report_file, 'r')
  for line in score_file:
    if "add_double" in line:
      value = re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',line)
      sum_average += int(value[0])
  return float(sum_average)/float(times) 
 
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

def run_make(times):
  print '>>> RUn apache test ...'
  os.chdir('/root/httpd-2.2.31')
  os.system('make clean')

  command = "(time sh -c \"make; make clean\") 2>> /mnt/report_file"
  directory = '/root/httpd-2.2.31'
  time_score = average_time_elapsed(command, times, directory)
  return time_score
 
def run_bw_mem(times):
  print '>>> Run bw_mem test ... '
  report_file = '/mnt/report_file'
  command = 'bw_mem 800M rd  2>> /mnt/report_file'
 
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
  command = './iozone -a -i 0 -i 1 -i 2 -s 2000000 -r 4096 2 >> /mnt/report_file'
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

file_name = 'F@email_score_full_'+str(st)

add_double_score = 'Add_double: '+  str(run_add_double(15)) + '\n'
write_report_file(add_double_score,file_name)

#bw_mem_score = 'Bw_mem: :'+  str(run_bw_mem(15)) + '\n'
#write_report_file(bw_mem_score,file_name)

bzip2_score = 'Bzip: '+str(run_bzip2(1)) + '\n'
write_report_file(bzip2_score, file_name)

cat_score = 'Cat: '+str(run_cat(15)) + '\n'
write_report_file(cat_score, file_name)

cachebench_score = 'Cachebench: '+str(run_cachebench(15)) + '\n' #
write_report_file(cachebench_score, file_name)

crypt_score = 'Ccrypt: ' + str(run_crypt(15)) + '\n'
write_report_file(crypt_score,file_name)

cp_score = 'Cp: '+str(run_cp(15)) + '\n'
write_report_file(cp_score,file_name)

dd_score = 'dd: '+str(run_dd(15)) + '\n'
write_report_file(dd_score, file_name)

grep_score = 'Grep: '+str(run_grep(15)) + '\n'
write_report_file(grep_score,file_name)

gzip_score = 'Gzip: '+str(run_gzip(15)) + '\n'
write_report_file(gzip_score, file_name)

iozone_score = run_iozone(15)
iozone_write = 'Iozone write sequential: '+str(iozone_score[0]) + '\n'
iozone_read = 'Iozone read sequential: '+ str(iozone_score[1]) + '\n'
iozone_wr_random = 'Iozone write_random: '+ str(iozone_score[2]) + '\n'
iozone_rd_random = 'Iozone read_random: '+ str(iozone_score[3]) + '\n'
write_report_file(iozone_write, file_name)
write_report_file(iozone_read, file_name)
write_report_file(iozone_wr_random, file_name)
write_report_file(iozone_rd_random, file_name)

make_score = 'Make: '+str(run_make(15)) + '\n'
write_report_file(make_score, file_name)

povray_score = 'Povray: '+str(run_povray(15)) + '\n'
write_report_file(povray_score, file_name)

print "send email"
send_email(file_name + ' Done!','')
