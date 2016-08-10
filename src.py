import subprocess
import re
import time
from Queue import Queue
import os
WRIO = "munin-run diskstats |grep vda_wrio.value"
RDIO = "munin-run diskstats |grep vda_rdio.value"
WRITE_LATENCY = "munin-run diskstats | grep avgwrwait"
READ_LATENCY = "munin-run diskstats | grep avgrdwait"


def run_metric(times):
  print "Colecting disk metrics"
  report_file = '/mnt/metric_report_file'
  command = "iostat -x -d vda > /mnt/metric_report_file 1 "+ str(times) 
  if os.path.isfile(report_file):
    os.remove(report_file)

  os.system(command)
  score_file = open(report_file)
  lines = score_file.readlines()
  sum_rdio = 0
  sum_wrio = 0
  sum_wr_await = 0
  sum_rd_await = 0 
  for s in lines:
    if 'vda' in s:
      line = re.findall(r'[-+]?([0-9]*\,[0-9]+|[0-9]+)',s)
      value_rdio = line[2]
      value_rdio = value_rdio.replace(",",".")

      value_wrio = line[3]
      value_wrio = value_wrio.replace(",",".")

      value_wr_await = line[9]
      value_wr_await = value_wr_await.replace(",",".")

      value_rd_await = line[10]
      value_rd_await = value_rd_await.replace(",",".") 


      sum_rdio += float(value_rdio)
      sum_wrio += float(value_wrio)
      sum_wr_await += float(value_wr_await)
      sum_rd_await += float(value_rd_await)
  
  avg_wrio = sum_wrio/times
  avg_rdio = sum_rdio/times
  avg_wr_latency = sum_wr_await/times
  avg_rd_latency = sum_rd_await/times

  print "write by second: "+ str(avg_wrio)
  print "read by second: "+ str(avg_rdio)
  print "write latency: "+ str(avg_wr_latency)
  print "read latency: "+str(avg_rd_latency)
   

#Colects metric from munin
def collect_metric(metric_munin): 
  cont = 0
  avg_sum = 0 
  colected_metric = subprocess.Popen(metric_munin,shell=True, stdout=subprocess.PIPE,)
  colected_metric = colected_metric.communicate()[0].rstrip('\n')
  metric_value =  re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',colected_metric)
  #print metric_munin,":",metric_value[0]
  if(metric_munin == WRIO or metric_munin == RDIO):
    return float( metric_value[0])	  
  else:
    return float(metric_value[1])
#calculates the average metric given time
def calculate_average(time_average,queue):
  cont = 0
  sum_wrio  = 0
  sum_rdio = 0
  sum_wr_time = 0
  sum_rd_time = 0
  while(cont < time_average):
     value_wrio = collect_metric(WRIO) 
     value_rdio = collect_metric(RDIO)
     write_latency = collect_metric(WRITE_LATENCY)
     read_latency = collect_metric(READ_LATENCY)
     
     sum_wrio += value_wrio
     sum_rdio += value_rdio
     sum_wr_time += write_latency
     sum_rd_time += read_latency
	 
     print value_wrio
     print value_rdio
     print write_latency
     print read_latency
     print cont
     time.sleep(1) #Collects every 1 second
     cont+=1  
  avg_wrio = sum_wrio/time_average
  avg_rdio = sum_rdio/time_average 
  avg_wr_latency = sum_wr_time/time_average
  avg_rd_latency = sum_rd_time/time_average
  print "media WRIO: ",avg_wrio
  print "media RDIO: ",avg_rdio 
  print "media write Latency:", avg_wr_latency
  print "media read latency:", avg_rd_latency
  print "\n" 
  queue.put(cont)
#calculate_average(2)  	
