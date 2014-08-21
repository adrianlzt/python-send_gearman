import gearman
import base64
import time

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.unique

gm_client = gearman.GearmanClient(['localhost:4730'])


host_name = "client1.com"
time = int(time.time())
rc = 0
output = "OK - status ok"
service = "check_cpu"

data="type=passive\n\
host_name=%s\n\
start_time=%s\n\
finish_time=%s\n\
latency=0.0\n\
return_code=%s\n\
output=%s" % (host_name, time, time, rc, output)

try:
  service
except NameError:
  print "Host check"
else:
  print "Service check"
  data += "\nservice_description="+service

data_enc = base64.b64encode(data)

completed_job_request = gm_client.submit_job("check_results", data_enc)
check_request_status(completed_job_request)
