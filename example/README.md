# 1. Unstructured log: default Python `logging` (Docker)

1. Build image:
  - `docker build -t py_log_script .`

2. Run container in background:
  - `docker run -d --name py_log_script --rm py_log_script`

3. Check logs:
  - `docker logs py_log_script`

Terminal output:

```log
  Print
  1 - 2020-08-23 18:39:13,782 - __main__ - DEBUG - Debug
  1 - 2020-08-23 18:39:13,783 - __main__ - INFO - Info
  1 - 2020-08-23 18:39:13,783 - __main__ - WARNING - Warning
  1 - 2020-08-23 18:39:13,783 - __main__ - CRITICAL - Critical
  1 - 2020-08-23 18:39:13,783 - __main__ - ERROR - Handled exception
  Traceback (most recent call last):
      File "example.py", line 24, in <module>
        1/0
  ZeroDivisionError: division by zero
```


4. Redirect Docker output into file:
  - Comment line `# time.sleep(60)`.
  - Uncomment line `# Unhandled exception`.
  - Rebuild image with command #1
  - `docker run --name py_log_script --rm py_log_script &> example.log`
    
    Note that we use `&>` redirect to save in file both STDOUT and STDERR.

File output:
```log
───────┬─────────────────────────────────────────────────────────────────────────────────────
       │ File: example.log
───────┼─────────────────────────────────────────────────────────────────────────────────────
   1   │ Print
   2   │ 1 - 2020-08-23 18:41:34,532 - __main__ - DEBUG - Debug
   3   │ 1 - 2020-08-23 18:41:34,532 - __main__ - INFO - Info
   4   │ 1 - 2020-08-23 18:41:34,532 - __main__ - WARNING - Warning
   5   │ 1 - 2020-08-23 18:41:34,532 - __main__ - CRITICAL - Critical
   6   │ 1 - 2020-08-23 18:41:34,532 - __main__ - ERROR - Handled exception
   7   │ Traceback (most recent call last):
   8   │   File "example.py", line 24, in <module>
   9   │     1/0
  10   │ ZeroDivisionError: division by zero
  11   │ ====================
  12   │ Traceback (most recent call last):
  13   │   File "example.py", line 31, in <module>
  14   │     sqrt(-1)  # !Uncomment to see that unhandled exceptions will appear in STDERR
  15   │ ValueError: math domain error
───────┴─────────────────────────────────────────────────────────────────────────────────────
```

5. You can also take a look on Docker stateful logs of the container.
Containers are stateless, and the logs are stored on the Docker host in JSON files by default.
But only if you don't use `--rm` flag when container starts.
This flag automatically remove the container when it exits (as well as logs and anonymous volumes)

- Uncomment line `# time.sleep(60)`.
- Run container: `docker run -d --name py_log_script py_log_script`
- Copy <container_id> from command output: `docker ps`
- Check logs in JSON format of this container on host:
  `cat /var/lib/docker/containers/<container_id>/<container_id>-json.log`
  Pay attention that:
      - logs and handled exception are in STDOUT
      - unhandled exception is in STDERR
      - each line is JSON-line, but multiline output (e.g. stack trace) formed as separate records,
        which is inconvenient and incorrect

JSON file output:

```log
───────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: 306c20c7b976a06cf49df300bbf8639c172b8b1d0d8b3c4e8bb8f8c0cccd317c-json.log
───────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ {"log":"Print\n","stream":"stdout","time":"2020-08-24T14:06:44.051727267Z"}
   2   │ {"log":"1 - 2020-08-24 14:06:44,051 - __main__ - DEBUG - Debug\n","stream":"stdout","time":"2020-08-24T14:06:44.051755203Z"}
   3   │ {"log":"1 - 2020-08-24 14:06:44,051 - __main__ - INFO - Info\n","stream":"stdout","time":"2020-08-24T14:06:44.051758586Z"}
   4   │ {"log":"1 - 2020-08-24 14:06:44,051 - __main__ - WARNING - Warning\n","stream":"stdout","time":"2020-08-24T14:06:44.051760858Z"}
   5   │ {"log":"1 - 2020-08-24 14:06:44,051 - __main__ - CRITICAL - Critical\n","stream":"stdout","time":"2020-08-24T14:06:44.051763034Z"}
   6   │ {"log":"1 - 2020-08-24 14:06:44,051 - __main__ - ERROR - Handled exception\n","stream":"stdout","time":"2020-08-24T14:06:44.051973
       │ 313Z"}
   7   │ {"log":"Traceback (most recent call last):\n","stream":"stdout","time":"2020-08-24T14:06:44.051982185Z"}
   8   │ {"log":"  File \"example.py\", line 24, in \u003cmodule\u003e\n","stream":"stdout","time":"2020-08-24T14:06:44.051984859Z"}
   9   │ {"log":"    1/0\n","stream":"stdout","time":"2020-08-24T14:06:44.051987337Z"}
  10   │ {"log":"ZeroDivisionError: division by zero\n","stream":"stdout","time":"2020-08-24T14:06:44.051989428Z"}
  11   │ {"log":"====================\n","stream":"stdout","time":"2020-08-24T14:06:44.051992382Z"}
  12   │ {"log":"Traceback (most recent call last):\n","stream":"stderr","time":"2020-08-24T14:06:44.05205322Z"}
  13   │ {"log":"  File \"example.py\", line 31, in \u003cmodule\u003e\n","stream":"stderr","time":"2020-08-24T14:06:44.052057884Z"}
  14   │ {"log":"    sqrt(-1)  # !Uncomment to see that unhandled exceptions will appear in STDERR\n","stream":"stderr","time":"2020-08-24T
       │ 14:06:44.052060356Z"}
  15   │ {"log":"ValueError: math domain error\n","stream":"stderr","time":"2020-08-24T14:06:44.052062609Z"}
───────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
```

# 2. Structured log: `JSON-log-formatter` (Docker, Loki)

* https://github.com/marselester/json-log-formatter
* Python 2/3 support

1. Run Loki environment from `/loki`, see `/loki/README.md`

2. Run script in container with Loki as log-driver:

```bash
$ docker build -t py_log_script .
$ docker run --log-driver loki --log-opt loki-url=http://localhost:3100/loki/api/v1/push --name py_log_script --rm py_log_script
```

3. See parsed JSON rows in Grafana dashboard: http://localhost:3000, see `/loki/README.md`, similar to:

```json
Print
{"extra_code": "De", "message": "Debug", "time": "2020-09-10T08:30:09.052853"}
{"extra_code": "In", "message": "Info", "time": "2020-09-10T08:30:09.053104"}
{"extra_code": "Wa", "message": "Warning", "time": "2020-09-10T08:30:09.053154"}
{"extra_code": "Cr", "message": "Critical", "time": "2020-09-10T08:30:09.053198"}
{"extra_code": "Ex", "message": "Handled exception", "time": "2020-09-10T08:30:09.053244", "exc_info": "Traceback (most recent call last):\n  File \"example.py\", line 24, in <module>\n    1/0\nZeroDivisionError: division by zero"}
Traceback (most recent call last):
  File "example.py", line 29, in <module>
    sqrt(-1)  # !Uncomment to see that unhandled exceptions will appear in STDERR
ValueError: math domain error
```

# 2.1 Structured log: `JSON-log-formatter` with custom format (Docker, Loki)

- same steps as in #2:

```json
Print
{"extra_code": "De", "nested": {"foo": 1, "bar": "bar"}, "message": "Dbg mes", "level": "DEBUG", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "In", "message": "Inf mes", "level": "INFO", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "Wa", "message": "Wrng mes", "level": "WARNING", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "Cr", "message": "Crtcl mes", "level": "CRITICAL", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "Ex", "message": "Handled exception", "level": "ERROR", "name": "__main__", "filename": "example.py", "funcName": "<module>", "exc_info": "Traceback (most recent call last):\n  File \"example.py\", line 29, in <module>\n    1/0\nZeroDivisionError: division by zero"}
Traceback (most recent call last):
  File "example.py", line 34, in <module>
    sqrt(-1)  # !Uncomment to see that unhandled exceptions will appear in STDERR
ValueError: math domain error

```

# 2.2 Structured log: `JSON-log-formatter` with custom format and application name in config (Docker, Loki)

- same steps as in #2:

```json
Print
{"extra_code": "De", "nested": {"foo": 1, "bar": "bar"}, "app": "myExampleApp", "message": "Dbg mes", "level": "DEBUG", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "In", "app": "myExampleApp", "message": "Inf mes", "level": "INFO", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "Wa", "app": "myExampleApp", "message": "Wrng mes", "level": "WARNING", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "Cr", "app": "myExampleApp", "message": "Crtcl mes", "level": "CRITICAL", "name": "__main__", "filename": "example.py", "funcName": "<module>"}
{"extra_code": "Ex", "app": "myExampleApp", "message": "Handled exception", "level": "ERROR", "name": "__main__", "filename": "example.py", "funcName": "<module>", "exc_info": "Traceback (most recent call last):\n  File \"example.py\", line 29, in <module>\n    1/0\nZeroDivisionError: division by zero"}
Traceback (most recent call last):
  File "example.py", line 34, in <module>
    sqrt(-1)  # !Uncomment to see that unhandled exceptions will appear in STDERR
ValueError: math domain error

```


# 3. Structured log: `python-json-logger` with custom format and application name in config (Docker, Loki)

* https://github.com/madzak/python-json-logger
* Python 2/3

1. Run Loki environment from `/loki`, see `/loki/README.md`

2. Run script in container with Loki as log-driver:

```bash
$ docker build -t py_log_script .
$ docker run --log-driver loki --log-opt loki-url=http://localhost:3100/loki/api/v1/push --name py_log_script --rm py_log_script
```

3. See parsed JSON rows in Grafana dashboard: http://localhost:3000, see `/loki/README.md`, similar to:

```json
Print
{"process": 1, "asctime": "2020-09-10 18:44:34,816", "name": "__main__", "levelname": "DEBUG", "message": "Dbg mes", "extra_code": "De", "nested": {"foo": 1, "bar": "bar"}, "app": "myExampleApp"}
{"process": 1, "asctime": "2020-09-10 18:44:34,816", "name": "__main__", "levelname": "INFO", "message": "Inf mes", "extra_code": "In", "app": "myExampleApp"}
{"process": 1, "asctime": "2020-09-10 18:44:34,817", "name": "__main__", "levelname": "WARNING", "message": "Wrng mes", "extra_code": "Wa", "app": "myExampleApp"}
{"process": 1, "asctime": "2020-09-10 18:44:34,817", "name": "__main__", "levelname": "CRITICAL", "message": "Crtcl mes", "extra_code": "Cr", "app": "myExampleApp"}
{"process": 1, "asctime": "2020-09-10 18:44:34,817", "name": "__main__", "levelname": "ERROR", "message": "Handled exception", "exc_info": "Traceback (most recent call last):\n  File \"example.py\", line 29, in <module>\n    1/0\nZeroDivisionError: division by zero", "extra_code": "Ex", "app": "myExampleApp"}
Traceback (most recent call last):
  File "example.py", line 34, in <module>
    sqrt(-1)  # !Uncomment to see that unhandled exceptions will appear in STDERR
ValueError: math domain error
```


# 4. Structured log: `structlog` with custom format and colored output

* https://www.structlog.org/en/16.0.0/index.html
* Python 3

1. Script only (plain log):
  
  ```bash
   $ cd ./script
   $ python3 -u structlog_example.py
  ``` 
  will give `colored` output to console:

  ```log
Print
2020-09-13 17:39:38 [debug    ] Dbg mes                        app=myApp code=De funcName=<module> lineno=15 nested={'foo': 1, 'bar': 'bar'} pathname=structlog_example.py process=6427 thread=4491980224
2020-09-13 17:39:38 [info     ] Inf mes                        app=myApp code=In funcName=<module> lineno=16 pathname=structlog_example.py process=6427 thread=4491980224
2020-09-13 17:39:38 [warning  ] Wrng mes                       app=myApp code=Wa funcName=<module> lineno=17 pathname=structlog_example.py process=6427 thread=4491980224
2020-09-13 17:39:38 [critical ] Crtcl mes                      app=myApp code=Cr funcName=<module> lineno=18 pathname=structlog_example.py process=6427 thread=4491980224
2020-09-13 17:39:38 [error    ] Handled exception              app=myApp bar=1 code=Ex funcName=handled_error_func lineno=27 pathname=structlog_example.py process=6427 thread=4491980224
Traceback (most recent call last):
  File "structlog_example.py", line 25, in handled_error_func
    1/0
ZeroDivisionError: division by zero
==========
Traceback (most recent call last):
  File "structlog_example.py", line 37, in <module>
    unhandled_error_func()
  File "structlog_example.py", line 33, in unhandled_error_func
    sqrt(-1)
ValueError: math domain error

  ```

2. Script only (JSON):
  
  - change `struclog_conf.py` -> `LOGGING['loggers']['handlers'] = ["prod"]` and run to see output in JSON:

  ```json
  Print
{"code": "De", "nested": {"foo": 1, "bar": "bar"}, "event": "Dbg mes", "app": "myApp", "funcName": "<module>", "thread": 4666121664, "pathname": "structlog_example.py", "lineno": 15, "process": 6861, "level": "debug", "timestamp": "2020-09-13 17:44:08"}
{"code": "In", "event": "Inf mes", "app": "myApp", "funcName": "<module>", "thread": 4666121664, "pathname": "structlog_example.py", "lineno": 16, "process": 6861, "level": "info", "timestamp": "2020-09-13 17:44:08"}
{"code": "Wa", "event": "Wrng mes", "app": "myApp", "funcName": "<module>", "thread": 4666121664, "pathname": "structlog_example.py", "lineno": 17, "process": 6861, "level": "warning", "timestamp": "2020-09-13 17:44:08"}
{"code": "Cr", "event": "Crtcl mes", "app": "myApp", "funcName": "<module>", "thread": 4666121664, "pathname": "structlog_example.py", "lineno": 18, "process": 6861, "level": "critical", "timestamp": "2020-09-13 17:44:08"}
{"code": "Ex", "bar": "1", "event": "Handled exception", "app": "myApp", "funcName": "handled_error_func", "thread": 4666121664, "pathname": "structlog_example.py", "lineno": 27, "process": 6861, "level": "error", "timestamp": "2020-09-13 17:44:08", "exception": "Traceback (most recent call last):\n  File \"structlog_example.py\", line 25, in handled_error_func\n    1/0\nZeroDivisionError: division by zero"}
==========
Traceback (most recent call last):
  File "structlog_example.py", line 37, in <module>
    unhandled_error_func()
  File "structlog_example.py", line 33, in unhandled_error_func
    sqrt(-1)
ValueError: math domain error
  ```

  3. Output will be the same with Docker + Loki because of JSON.