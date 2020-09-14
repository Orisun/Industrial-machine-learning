from telegraf.client import TelegrafClient

client = TelegrafClient(host="127.0.0.1", port=8089)

# measurement_name是表名，values=1代表正样本，values=0代表负样本。tags上会建索引，pageno代表在第几页展现，position代表在页内的位置。
client.metric(measurement_name="click_ratio", values=1, tags={"pageno": 1, "position": 1})
client.metric("click_ratio", 0, {"pageno": 1, "position": 2})
client.metric("click_ratio", 0, {"pageno": 1, "position": 1})
client.metric("click_ratio", 1, {"pageno": 2, "position": 1})