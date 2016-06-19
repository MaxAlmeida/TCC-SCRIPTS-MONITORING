import subprocess
import re
import time
WRIO = "munin-run diskstats |grep vda_wrio.value"
RDIO = "munin-run diskstats |grep vda_rdio.value"

#Colects metric from munin
def collect_metric(metric_munin):
  cont = 0
  avg_sum = 0 
  colected_metric = subprocess.Popen(metric_munin,shell=True, stdout=subprocess.PIPE,)
  colected_metric = colected_metric.communicate()[0].rstrip('\n')
  metric_value =  re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',colected_metric)
  print metric_munin,":",metric_value[0]
  return float( metric_value[0])	  
 
#calculates the average metric given time
def calculate_average(time_average):
  cont = 0
  sum_wrio  = 0
  sum_rdio = 0
  while(cont < time_average):
     value_wrio = collect_metric(WRIO) 
     value_rdio = collect_metric(RDIO)
     sum_wrio += value_wrio
     sum_rdio += value_rdio	 
     print "\n"
     time.sleep(1) #Collects every 1 second
     cont+=1
  avg_wrio = sum_wrio/time_average
  avg_rdio = sum_rdio/time_average 

  print "media WRIO: ",avg_wrio
  print "media RDIO: ",avg_rdio 

calculate_average(10)  	
