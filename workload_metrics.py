import workload as app
import thread
import src as metric
import multiprocessing
from Queue import Queue
import os


app.run_bzip2(1000)
app.run_crypt(1000)
app.run_cat(1000)
app.run_cp(1000)
app.run_dd(10000)
app.run_grep(1000)
app.run_gzip(1000)
#metric = multiprocessing.Process(target=metric.run_metric, args=(120,))
#application = multiprocessing.Process(target=app.run_dd, args=(10000,))
#metric = multiprocessing.Process(target=metric.calculate_average, args=(12,queue))
#application.start()
#metric.start()

#print metric.exitcode
#while(1):
 #if(metric.exitcode == 0):
  #application.terminate()
  #break

