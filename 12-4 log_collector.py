import os
from absl import app
from absl import flags
from apscheduler.schedulers.background import BackgroundScheduler
from socket import *
from datetime import datetime, timedelta
import time

FLAGS = flags.FLAGS
flags.DEFINE_string("port", "0", "which port to listen")
flags.DEFINE_string("logfile", "", "write udp data to which file")
flags.DEFINE_string(
    "filetype", "1", "1 represent text file, 2 represent binary file")

writer = None
# 与发送方约定好一个UDP数据报文的最大长度
MAX_UDP_DATA_LEN = 10240

def reset_writer(out_file, file_type):
    global writer

    postfix = datetime.now().strftime("%Y%m%d")
    if file_type == 1:
        # 以追回方式打开文本文件，若文件不存在则创建之
        writer = open(out_file+"."+postfix, "a+")
    else:
        # 以追回方式打开二进制文件，若文件不存在则创建之
        writer = open(out_file+"."+postfix, "ab+")

def main(argv):
    del argv
    port = 0
    if FLAGS.port:
        try:
            port = int(FLAGS.port)
        except:
            pass
    if port < 1024:
        # Linux普通用户不能使用1024以下的端口
        print("plesae use a port more than 1024")
        exit(0)

    logfile = FLAGS.logfile
    if not logfile:
        print("plesae assign an output file for udp log")
        exit(0)

    filetype = 1
    if FLAGS.filetype:
        try:
            filetype = int(FLAGS.filetype)
        except:
            pass
    if filetype not in [1, 2]:
        print(
            "plesae input a valid filetype, 1 represent text file, 2 represent binary file")
        exit(0)

    reset_writer(logfile, filetype)

    root_path = os.path.dirname(logfile)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=reset_writer, args=(logfile, filetype,), trigger='cron', hour=0)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()

    s = socket(AF_INET, SOCK_DGRAM)  # UDP
    s.bind(('0.0.0.0', port))
    while True:
        data, _ = s.recvfrom(MAX_UDP_DATA_LEN)
        writer.write(data)
        writer.flush()

    writer.close()
    s.close()

if __name__ == "__main__":
    app.run(main)