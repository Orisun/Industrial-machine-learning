import simplejson
from flumelogger import handler
import logging
import logging.config

FLUME_HOST = "127.0.0.1"
REQUEST_PORT = 1234
FEATURE_PORT = 2345
SHOW_PORT = 3456
CLICK_PORT = 4567

LOG_DELIMITER = b"\xba\x11\x7f\xc3\x57"

def create_logger(port, name):
    formater = logging.Formatter("%(message)s")
    halr = handler.FlumeHandler(host=FLUME_HOST, port=port)
    halr.setFormatter(formater)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(halr)

request_logger = create_logger(REQUEST_PORT, "request_logger")
feature_logger = create_logger(FEATURE_PORT, "feature_logger")
show_logger = create_logger(SHOW_PORT, "show_logger")
click_logger = create_logger(CLICK_PORT, "click_logger")

def send_request(request):
    # protobuf序列化为字节流，再加上特定分隔符
    bytes = request.SerializeToString() + LOG_DELIMITER
    request_logger.info(bytes)

def send_feature(feature):
    # protobuf序列化为字节流，再加上特定分隔符
    bytes = feature.SerializeToString() + LOG_DELIMITER
    feature_logger.info(bytes)

def send_show(show):
    # 序列化为json字符串，再加一个换行符
    json = simplejson.dumps(show.__dict__) + "\n"
    show_logger.info(json)

def send_click(click):
    # 序列化为json字符串，再加一个换行符
    json = simplejson.dumps(click.__dict__) + "\n"
    click_logger.info(json)