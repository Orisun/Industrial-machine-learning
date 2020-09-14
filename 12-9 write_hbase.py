import happybase
from log_merger import sample_generator

conn = happybase.Connection(host='localhost', table_prefix="namespace", table_prefix_separator=b':', transport='framed', protocol='compact')
request_table = conn.table("request")
corpus_table = conn.table("corpus")

for request, feature, show, click, tag in sample_generator():
    # 写request表
    rowkey = str(request.uid) + "_" + request.traceid
    data = {"request:location": request.location, "request:request_time": str(request.request_time)}
    request_table.put(rowkey, data)
    # 写corpus表
    rowkey = str(request.uid) + "_" + request.traceid + "_" + str(show.itemid)
    data = {"feature:gen_feature_time": str(feature.gen_feature_time), "feature:gender": str(feature.gender), "feature:price": str(feature.price), "show:show_time": str(show.show_time), "show:position": str(show.position)}
    if tag:
        data["click:click_time"] = str(click.click_time)
    corpus_table.put(rowkey, data)