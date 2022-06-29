import threading

import pymysql

conn_xx = pymysql.connect(host='192.168.31.5',
                          user='root',
                          port=3306,
                          password='ti9#aN%^^ToqacQD',
                          db='fosseye',
                          charset='utf8mb4')
cur1 = conn_xx.cursor()

con2 = pymysql.connect(host='192.168.31.17',
                       port=3306,
                       user='root',
                       password='ti9#aN%^^ToqacQD',
                       db='lj_id',
                       charset='utf8')
cur2 = con2.cursor()


def main(th):
    conn_xx.ping(reconnect=True)
    con2.ping(reconnect=True)
    sql1 = 'select id, dependency_package_name from pip_package_dependencies where dependency_lj_package_id is null limit {},{}'.format(
        th * 500000, 500000)

    cur1.execute(sql1)

    all_data = cur1.fetchall()
    for i in all_data:
        _id = i[0]
        p_n = i[1]
        sql2 = 'select id from lj_id_map_package where package_name=%s and type = "pip"'
        cur2.execute(sql2, [p_n])
        try:
            lj_id = cur2.fetchone()[0]
        except:
            print('mei cha dao')
            continue
        print(lj_id)
        sql3 = 'update pip_package_dependencies set dependency_lj_package_id=%s where id=%s'
        cur1.execute(sql3, [lj_id, _id])
        conn_xx.commit()


for i in range(1):
    t = threading.Thread(target=main, args=(i,))
    t.start()
