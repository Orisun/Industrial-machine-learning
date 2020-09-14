from expiringdict import ExpiringDict
import heapq
from log_generator import request_generator, feature_generator, show_generator, click_generator
import threading
import time

class Corpus(object):
    """feature、show、click这3种数据可以按traceid+itemid进行合并
    """
    feature = None
    show = None
    click = None

TIME_WINDOW = 600  # 时间窗口设为10分钟
corpus_in_time_window = []
corpus_item_dict = dict()  # 两层嵌套的dict，外层dict的key是traceid，内层dict的key是itemid，value是Corpus
request_dict = ExpiringDict(max_len=100000,
                            max_age_seconds=1.2 * TIME_WINDOW)  # traceid作为key，value是Request。Request没有itemid，所以单独存到一个dict里

def receive_request():
    for request in request_generator():
        traceid = request.traceid
        request_dict[traceid] = request  # 存入request_dict

def receive_feature():
    for feature in feature_generator():
        traceid = feature.traceid
        itemid = feature.itemid
        corpus_dict = corpus_item_dict.get(traceid)
        if not corpus_dict:
            corpus_dict = dict()
            corpus = Corpus()
            corpus.feature = feature
            corpus_dict[itemid] = corpus
            corpus_item_dict[traceid] = corpus_dict  # 存入corpus_dict
            feature_time = feature.gen_feature_time
            heapq.heappush(corpus_in_time_window, (feature_time, traceid))  # 存入小根堆，以数据生成时间作为排序依据，同时把traceid也存到树的节点中
        else:
            corpus = corpus_dict.get(itemid)
            if not corpus:
                corpus = Corpus()
                corpus.feature = feature
                corpus_dict[itemid] = corpus
            else:
                corpus.feature = feature

def receive_show():
    for show in show_generator():
        traceid = show.traceid
        itemid = show.itemid
        corpus_dict = corpus_item_dict.get(traceid)
        if not corpus_dict:
            corpus_dict = dict()
            corpus = Corpus()
            corpus.show = show
            corpus_dict[itemid] = corpus
            corpus_item_dict[traceid] = corpus_dict  # 存入corpus_dict
            show_time = show.show_time
            heapq.heappush(corpus_in_time_window, (show_time, traceid))  # 存入小根堆，以日志生成时间作为排序依据，同时把traceid也存到树的节点中
        else:
            corpus = corpus_dict.get(itemid)
            if not corpus:
                corpus = Corpus()
                corpus.show = show
                corpus_dict[itemid] = corpus
            else:
                corpus.show = show

def receive_click():
    for click in click_generator():
        traceid = click.traceid
        itemid = click.itemid
        corpus_dict = corpus_item_dict.get(traceid)
        if not corpus_dict:
            corpus_dict = dict()
            corpus = Corpus()
            corpus.click = click
            corpus_dict[itemid] = corpus
            corpus_item_dict[traceid] = corpus_dict  # 存入corpus_dict
            click_time = click.click_time
            heapq.heappush(corpus_in_time_window, (click_time, traceid))  # 存入小根堆，以数据生成时间作为排序依据，同时把traceid也存到树的节点中
        else:
            corpus = corpus_dict.get(itemid)
            if not corpus:
                corpus = Corpus()
                corpus.click = click
                corpus_dict[itemid] = corpus
            else:
                corpus.click = click

def sample_generator():
    """组合4种日志，生成样本
    """
    while True:
        if len(corpus_in_time_window) == 0:
            time.sleep(0.1)
            continue  # corpus_in_time_window暂时为空，呆会儿还会有数据进来
        window_begin = time.time() - TIME_WINDOW  # 时间窗口的起始点
        earliest_corpus = corpus_in_time_window[0]  # 取出小根堆的堆顶元素
        if window_begin < earliest_corpus[0]:  # 堆顶元素在时间窗口以内
            time.sleep(0.1)
            continue  # 什么都不做

        # 堆顶元素在时间窗口以外
        heapq.heappop(corpus_in_time_window)  # 删除堆顶元素
        traceid = earliest_corpus[1]  # 取出堆顶元素的traceid
        request = request_dict.get(traceid)
        if request:
            del request_dict[traceid]  # 从request_dict中删除，释放内存
        corpus_dict = corpus_item_dict.get(traceid)
        if corpus_dict:
            for itemid, corpus in corpus_dict.items():
                feature = corpus.feature
                show = corpus.show
                click = corpus.click
                if show:
                    if click:  # 正样本
                        if request:
                            yield (request, feature, show, click, True)
                    else:  # 负样本
                        if request:
                            yield (request, feature, show, click, False)

request_thread=threading.Thread(target=receive_request,)
request_thread.start()
feature_thread=threading.Thread(target=receive_feature,)
feature_thread.start()
show_thread=threading.Thread(target=receive_show,)
show_thread.start()
click_thread=threading.Thread(target=receive_click,)
click_thread.start()

if __name__ == "__main__":
    for request, feature, show, click, tag in sample_generator():
        # 打印样本特征和样本标签
        print feature.uid, feature.itemid, request.request_time, request.location, feature.gender, feature.price, show.position, "1" if tag else "0"