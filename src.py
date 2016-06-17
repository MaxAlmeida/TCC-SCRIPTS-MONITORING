import subprocess
import re
import time

cont = 0
avg_sum = 0 
while cont < 300:
  process = subprocess.Popen("munin-run diskstats |grep vda_wrio.value",shell=True, stdout=subprocess.PIPE,)
  output = process.communicate()[0].rstrip('\n')
  final =  re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',output)
  avg_sum +=  float(final[0])
  print final[0]
  time.sleep(1) 		
  cont+=1
   
avg =  avg_sum/300
print "media: ", avg
   
