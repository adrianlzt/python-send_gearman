import gearman
import base64
import time
import rijndael

# Params
host_name = "m2m_client1.com"
time = int(time.time())
rc = 0
output = "Cosa de output"
service = "check_cpu" # Optional
key = 'clave123' # Optional



KEY_SIZE = 32
BLOCK_SIZE = 16

def encrypt(key, plaintext):
    padded_key = key.ljust(KEY_SIZE, '\0')
    padded_text = plaintext + (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * '\0'

    # could also be one of
    #if len(plaintext) % BLOCK_SIZE != 0:
    #    padded_text = plaintext.ljust((len(plaintext) / BLOCK_SIZE) + 1 * BLOCKSIZE), '\0')
    # -OR-
    #padded_text = plaintext.ljust((len(plaintext) + (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE)), '\0')

    r = rijndael.rijndael(padded_key, BLOCK_SIZE)

    ciphertext = ''
    for start in range(0, len(padded_text), BLOCK_SIZE):
        ciphertext += r.encrypt(padded_text[start:start+BLOCK_SIZE])

    encoded = base64.b64encode(ciphertext)

    return encoded

def check_request_status(job_request):
    if job_request.complete:
        print "Job %s finished!  Result: %s - %s" % (job_request.job.unique, job_request.state, job_request.result)
    elif job_request.timed_out:
        print "Job %s timed out!" % job_request.unique
    elif job_request.state == JOB_UNKNOWN:
        print "Job %s connection failed!" % job_request.unique


gm_client = gearman.GearmanClient(['localhost:4730'])

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

try:
  key
except NameError:
  data_enc = base64.b64encode(data)
  print "No encryption"
else:
  data_enc = encrypt(key, data)
  print "Encryption"

completed_job_request = gm_client.submit_job("check_results", data_enc)
check_request_status(completed_job_request)
