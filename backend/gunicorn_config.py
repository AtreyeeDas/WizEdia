import multiprocessing
import os

# Number of workers = (2 x $num_cores) + 1
workers = (2 * multiprocessing.cpu_count()) + 1

# The socket to bind
bind = '0.0.0.0:' + os.environ.get('PORT', '5000')

# Use eventlet worker class
worker_class = 'eventlet'

# Number of threads per worker
threads = 2

# Timeout (in seconds)
timeout = 120

# Keep-alive (in seconds)
keepalive = 5

# Logging
accesslog = '-'  # Log to stdout
errorlog = '-'   # Log to stderr
loglevel = 'info'

# Maximum requests per worker
max_requests = 1000
max_requests_jitter = 50

# Worker connections
worker_connections = 1000
