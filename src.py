import subprocess
import re
import time


def colect_metric(amount):
  cont = 0
  avg_sum = 0 
  while cont < amount:
    colected_metric = subprocess.Popen("munin-run diskstats |grep vda_wrio.value",shell=True, stdout=subprocess.PIPE,)
    colected_metric = colected_metric.communicate()[0].rstrip('\n')
    metric_value =  re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',colected_metric)
    avg_sum +=  float(metric_value[0])
    print metric_value[0]
    time.sleep(1) 		
    cont+=1
   
  avg =  avg_sum/amount
  print "media: ", avg
  
colect_metric(5) 
