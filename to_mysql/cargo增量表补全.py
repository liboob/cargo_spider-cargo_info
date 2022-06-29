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

sql1 = 'select id, lj_package_id from cargo_package_dependencies_increment'
cur1.execute(sql1)

all_data = cur1.fetchall()
for i in all_data:
    _id = i[0]
    lj_id = i[1]
    sql2 = 'select package_name from lj_id_map_package where id=%s and type = "cargo"'
    cur2.execute(sql2, [lj_id])
    p_n = cur2.fetchone()[0]
    print(p_n)
    sql3 = 'update cargo_package_dependencies_increment set package_name=%s where id=%s'
    cur1.execute(sql3, [p_n, _id])
    conn_xx.commit()
