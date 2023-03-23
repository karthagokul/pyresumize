import sys
import os
from os import path
from glob import glob
import signal

sys.path.append("src")
from pyresumize.resume_processor import ResumeEngine


# Profiling import
from time import time
from functools import wraps
import platform, socket, re, uuid, json, psutil, logging

# Profile over


# Functions For Profiling
def getSystemInfo():
    try:
        info = {}
        info["Platform"] = platform.system()
        info["Platform-release"] = platform.release()
        info["Platform-version"] = platform.version()
        info["Architecture"] = platform.machine()
        info["Hostname"] = socket.gethostname()
        info["Ip-address"] = socket.gethostbyname(socket.gethostname())
        info["Mac-address"] = ":".join(re.findall("..", "%012x" % uuid.getnode()))
        info["Processor"] = platform.processor()
        info["RAM"] = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
        return json.dumps(info)
    except Exception as e:
        logging.exception(e)


def _log(message):
    print("[PyResumize Profiler] {function_name} {total_time:.3f}".format(**message))
    print(getSystemInfo())


def simple_time_tracker(log_fun):
    def _simple_time_tracker(fn):
        @wraps(fn)
        def wrapped_fn(*args, **kwargs):
            start_time = time()
            try:
                result = fn(*args, **kwargs)
            finally:
                elapsed_time = time() - start_time

                # log the result
                log_fun(
                    {
                        "function_name": fn.__name__,
                        "total_time": elapsed_time,
                    }
                )

            return result

        return wrapped_fn

    return _simple_time_tracker


def process_resume(file_name):
    r_parser = ResumeEngine()
    r_parser.set_custom_keywords_folder("data")
    return r_parser.process_resume(file_name)


def find_ext(dr, ext):
    files = []
    files = [
        os.path.join(dp, f) for dp, dn, filenames in os.walk(dr) for f in filenames if os.path.splitext(f)[1] == ext
    ]
    return files


def signal_handler(sig, frame):
    """Need to capture the Control-C especially when any module is in live processing mode"""
    sys.exit(0)


@simple_time_tracker(_log)
def main():
    """find the files in a given folder with extension pdf and process those"""
    if len(sys.argv) < 2:
        print("Error : The resume folder to be specified as command line argument")
        sys.exit(-1)
    foldername = str(sys.argv[1])
    files = find_ext(foldername, ".pdf")
    counter = 0
    for file in files:
        counter += 1
        print("\n[%d/%d] Filename: %s " % (counter, len(files), file))
        result = process_resume(file)
        print(result)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    # Below line is required , Related to PY bug https://bugs.python.org/issue35935
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
