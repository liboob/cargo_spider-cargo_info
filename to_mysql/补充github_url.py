import pymongo
import pymysql

# 117数据库链接
client = pymongo.MongoClient('mongodb://admin:pFFOdfJR8*I3WteU@192.168.31.5:27017')
db = client['Cargo']
collection = db['Cargo_info_versions']

conn_xx = pymysql.connect(host='192.168.31.5',
                          user='root',
                          port=3306,
                          password='ti9#aN%^^ToqacQD',
                          db='fosseye',
                          charset='utf8mb4')

cur = conn_xx.cursor()


def main():
    sql = 'select id, package_name from cargo_packages_info where github_url is null'
    cur.execute(sql)
    datas = cur.fetchall()
    for data in datas:
        _id = data[0]
        p = data[1]
        res = collection.find_one({"id": p})
        if res:
            url = res.get('repository')
            if url:
                print(_id, p, url)
                sql2 = 'update cargo_packages_info set github_url=%s where id=%s'
                cur.execute(sql2, [url, _id])
                conn_xx.commit()

if __name__ == '__main__':
    main()
