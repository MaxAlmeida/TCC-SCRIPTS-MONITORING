import subprocess
import datetime
import re
import time
from Queue import Queue
import os
import workload as app
WRIO = "munin-run diskstats |grep vda_wrio.value"
RDIO = "munin-run diskstats |grep vda_rdio.value"
WRITE_LATENCY = "munin-run diskstats | grep avgwrwait"
READ_LATENCY = "munin-run diskstats | grep avgrdwait"


def run_metric(times, application):
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

      value_wr_await = line[10]
      value_wr_await = value_wr_await.replace(",",".")

      value_rd_await = line[9]
      value_rd_await = value_rd_await.replace(",",".") 


      sum_rdio += float(value_rdio)
      sum_wrio += float(value_wrio)
      sum_wr_await += float(value_wr_await)
      sum_rd_await += float(value_rd_await)
  
  avg_wrio = sum_wrio/times
  avg_rdio = sum_rdio/times
  avg_wr_latency = sum_wr_await/times
  avg_rd_latency = sum_rd_await/times

  #st  = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d-%H%M')
  file_name = 'B@inactive__metric'#+str(st)
  
  app.write_report_file(">>>> "+application+ " <<<<"+"\n\n",file_name)
  app.write_report_file("write by second: "+ str(avg_wrio)+'\n',file_name)
  app.write_report_file("read by second: "+ str(avg_rdio)+'\n',file_name)
  app.write_report_file("write latency: "+ str(avg_wr_latency)+'\n',file_name)
  app.write_report_file("read latency: "+str(avg_rd_latency)+'\n',file_name)
  app.write_report_file("\n\n",file_name)  
