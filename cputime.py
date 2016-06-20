import subprocess
import time
import re
cont = 0
initial = subprocess.Popen("virsh dominfo one-688 | grep time", shell=True,stdout=subprocess.PIPE,)
initial = initial.communicate()[0].rstrip('\n')
initial_value =  re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',initial)
print initial_value[0]
time.sleep(60)
final = subprocess.Popen("virsh dominfo one-688 | grep time", shell=True,stdout=subprocess.PIPE,)
final = final.communicate()[0].rstrip('\n')
final_value =  re.findall(r'[-+]?([0-9]*\.[0-9]+|[0-9]+)',final)
print final_value[0]
print "CPU average: ",(float(final_value[0])-float(initial_value[0]))/60
