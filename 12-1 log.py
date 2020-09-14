class Log(object):
    traceid = ""  # 前端每次请求算法服务时生成一个唯一的traceid，即算法服务本次返回的这一批item共用一个traceid
    uid = 0  # 用户id
    itemid = 0  # 物品id

class Show(Log):
    show_time = 0  # 展现时间
    position = 0  # 在列表中的第几个位置展现

class Click(Log):
    click_time = 0  # 点击时间