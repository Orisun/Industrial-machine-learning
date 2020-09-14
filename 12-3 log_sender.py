from socket import *
import struct
import simplejson

HOST = "127.0.0.1"
REQUEST_PORT = 1234
FEATURE_PORT = 2345
SHOW_PORT = 3456
CLICK_PORT = 4567

LOG_DELIMITER = b"\xba\x11\x7f\xc3\x57"

s = socket(AF_INET, SOCK_DGRAM)  # UDP

def send_request(request):
    # protobuf序列化为字节流，再加上特定分隔符
    bytes = request.SerializeToString() + LOG_DELIMITER
    s.sendto(bytes, (HOST, REQUEST_PORT))

def send_feature(feature):
    # protobuf序列化为字节流，再加上特定分隔符
    bytes = feature.SerializeToString() + LOG_DELIMITER
    s.sendto(bytes, (HOST, FEATURE_PORT))

def send_show(show):
    # 序列化为json字符串，再加一个换行符
    json = simplejson.dumps(show.__dict__) + "\n"
    # 用struct转为字节流
    bytes = struct.pack("{:d}s".format(len(json)), json)
    s.sendto(bytes, (HOST, SHOW_PORT))

def send_click(click):
    # 序列化为json字符串，再加一个换行符
    json = simplejson.dumps(click.__dict__) + "\n"
    # 用struct转为字节流
    bytes = struct.pack("{:d}s".format(len(json)), json)
    s.sendto(bytes, (HOST, CLICK_PORT))

def close():
    s.close()