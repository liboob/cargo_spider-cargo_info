import json
import threading

import Cargo_packages_info as INFO
import Cargo_package_dependencie as DEP
import common_utils.common_methods as CM

package_type = 'cargo'


def mysql_monitor(package_type):
    print('开始监控入库队列')
    CM.consuming_message(package_type, 'mysql', mysql_main)


def mysql_main(channel, method, header_props, message):
    msg = str(message, encoding='utf-8')
    try:
        package_name = msg
        print(package_name)
    except:
        msg_t = json.loads(msg)
        package_name = msg_t['package_name']
        print(package_name)
    INFO.info_main(package_name, package_type)
    # get_lj_package_id = CM.LjIdClass()
    # get_lj_package_id(package_name, package_type, 'cargo_spider_queue')
    DEP.dep_main(package_name, package_type)
    channel.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    # while 1:
    #     if threading.activeCount() < 6:
    #         t = threading.Thread(target=mysql_monitor, args=(package_type,))
    #         t.start()
    mysql_monitor('cargo')
