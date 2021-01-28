from .models import Operation
from .caculator import Caculator
import urllib.request
import re

# 拉取当前数据
def query_realtime_price(list):
    to_return = {}
    if len(list) == 0:
        return to_return

    url = 'https://stockcrawl.iakira.moe/list='
    for code in list:
        url = url+code+','
    print(url) 
    res_data=urllib.request.urlopen(url).read()
    # print(res_data)
    res_array = str(res_data,encoding="gb18030").split(';')
    print(res_array)
    for i,single in enumerate(res_array):
        if len(single) > 10:
            content = re.search(r'\"([^\"]*)\"',single).group()
            single_info = eval(content).split(',')
            print(len(single_info))
            if len(single_info) > 4:
                offset = float(single_info[3]) - float(single_info[2])
                offset_ratio = "%.2f%%" % (offset/float(single_info[2]) * 100) 
                single_real_time = [single_info[0],single_info[3],offset,offset_ratio,single_info[2]] #名称，现价，涨跌额，涨跌幅，昨收
            
                to_return[list[i]] = single_real_time
    #print(to_return)
    return to_return

# 操作记录的预处理
def format_operations(list):
    to_return = {}
    for operation in list:
        if ((operation.platformType !=  None) and (operation.platformType != '')):
              operation.code = operation.platformType + operation.code
        if (operation.code not in to_return.keys()):
           to_return[operation.code] = []
        to_return[operation.code].append(operation)

    return to_return

#指标计算
def caculate_target(operation_list,realtime_list):
    caculator = Caculator(operation_list,realtime_list)

    return caculator.caculate_target()

