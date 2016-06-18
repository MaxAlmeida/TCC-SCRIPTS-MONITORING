import subprocess
import re
import time
WRIO = "munin-run diskstats |grep vda_wrio.value"
RDIO = "munin-run diskstats |grep vda_rdio.value"
def collect_metric(amount,metric_munin):
  cont = 0
  avg_sum = 0 
  colected_metric = subprocess.Popen(metric_munin,shell=True, stdout=subprocess.PIPE,)
  colected_metric = colected_metric.communicate()[0].rstrip('\n')
  metric_value =  re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',colected_metric)
  print metric_munin,":",metric_value[0]
  return float( metric_value[0])	  
 
 
cont = 0
sum_wrio  = 0
sum_rdio = 0
while(cont < 10):
    value_wrio = collect_metric(5,WRIO) 
    value_rdio = collect_metric(5,RDIO)
    sum_wrio += value_wrio
    sum_rdio += value_rdio	 
    print "\n"
    time.sleep(0.5)
    cont+=1
avg_wrio = sum_wrio/10
avg_rdio = sum_rdio/10 

print "media WRIO: ",avg_wrio
print "media RDIO: ",avg_rdio   	
