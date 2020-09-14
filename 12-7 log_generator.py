from rpc_pb2 import Request, Feature
from log import Show, Click
from log_sender import LOG_DELIMITER
from bytebuffer import ByteBuffer
from log_collector import MAX_UDP_DATA_LEN
import simplejson
from datetime import datetime

REQUEST_LOG_FILE = "/path/to/request.log"
FEATURE_LOG_FILE = "/path/to/feature.log"
SHOW_LOG_FILE = "/path/to/show.log"
CLICK_LOG_FILE = "/path/to/click.log"

def byte_log_generator(log_file):
    postfix = datetime.now().strftime("%Y%m%d")
    with open(log_file + "." + postfix, "rb") as f_in:
        delimiter_len = len(LOG_DELIMITER)
        bf = ByteBuffer.allocate(MAX_UDP_DATA_LEN)
        while True:
            curr_position = f_in.tell()
            n = 0
            # 重试10次，尽量把buffer读满
            for _ in xrange(10):
                n += bf.read_from_file(f_in)
                if bf.get_remaining() == 0:
                    break
            if n <= 0:
                break

            bf.flip()  # bf由写入变为读出状态，即把position置为0

            idx = 0
            target = LOG_DELIMITER[idx]  # 当前要寻找LOG_DELIMITER中的哪个字符

            bf.mark()  # 记下当前位置，reset时会回到这个位置
            begin = 0  # 以delimiter结束上一段后，下一段的开始位置
            length = 0  # 上一次delimiter结束后，又从buffer中读了几个字节

            while True:
                if bf.get_remaining() == 0:
                    break
                b = bf.get_bytes(1)[0]  # 逐个字节地读buffer
                length += 1
                if b == target:
                    idx += 1
                    if idx == delimiter_len:  # 遇到了完整的LOG_DELIMITER
                        begin = bf.get_position()  # 下一次读buffer的开始位置
                        bf.reset()  # 回到本段的开始位置
                        idx = 0
                        bytes = bf.get_bytes(length - delimiter_len)
                        yield bytes
                        bf.set_position(begin)  # 显式回到指定位置
                        bf.mark()
                        length = 0
                    target = LOG_DELIMITER[idx]  # 下一个寻找目标
                else:
                    if idx > 0:  # 重置idx和target
                        idx = 0
                        target = LOG_DELIMITER[idx]

            f_in.seek(curr_position + begin)
            bf.clear()  # 回到0位置

def request_generator():
    for bytes in byte_log_generator(REQUEST_LOG_FILE):
        request = Request()
        try:
            # protobuf反序列化
            request.ParseFromString(bytes)
        except:
            pass
        else:
            yield request

def feature_generator():
    for bytes in byte_log_generator(FEATURE_LOG_FILE):
        feature = Feature()
        try:
            # protobuf反序列化
            feature.ParseFromString(bytes)
        except:
            pass
        else:
            yield feature

def text_log_generator(log_file):
    postfix = datetime.now().strftime("%Y%m%d")
    with open(log_file + "." + postfix) as f_in:
        for line in f_in:
            yield line.strip()

def show_generator():
    for text in text_log_generator(SHOW_LOG_FILE):
        # json反序列化
        dic = simplejson.loads(text)
        traceid = dic.get("traceid", "")
        uid = dic.get("uid", 0)
        itemid = dic.get("itemid", 0)
        show_time = dic.get("show_time", 0)
        position = dic.get("position", 0)
        if traceid and uid and itemid and show_time:
            show = Show()
            show.traceid = traceid
            show.uid = uid
            show.itemid = itemid
            show.show_time = show_time
            show.position = position
            yield show

def click_generator():
    for text in text_log_generator(CLICK_LOG_FILE):
        # json反序列化
        dic = simplejson.loads(text)
        traceid = dic.get("traceid", "")
        uid = dic.get("uid", 0)
        itemid = dic.get("itemid", 0)
        click_time = dic.get("click_time", 0)
        if traceid and uid and itemid and click_time:
            click = Click()
            click.traceid = traceid
            click.uid = uid
            click.itemid = itemid
            click.click_time = click_time
            yield click