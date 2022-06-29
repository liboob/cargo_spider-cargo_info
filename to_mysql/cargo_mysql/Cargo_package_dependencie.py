import pymongo
import pymysql
import hashlib

from common_utils.common_methods import *
from common_utils.env_settings import *
from package.lj_sqlpackage import *

insert_to_db_tool = SqlTool(host='mysql.center.spdx.cn', port=3306, user='data_center', pwd='123456', db='52KIXFwbh4zG',
                            charset='utf8mb4')

logger = LoggerClass('python-package', 'cargo', is_print=1)


# def get_insert_sql(insert_data, table_name):
#     datas = insert_data.items()
#     insert_data_key = ','.join([x[0] for x in datas])
#     data_value = [x[1] for x in datas]
#     num_s = ('%s,' * len(insert_data))[:-1]
#     update_data_key = ','.join([x[0] + '=%s' for x in datas])
#     sql_insert = f'INSERT INTO `{table_name}`({insert_data_key}) VALUES({num_s}) ON DUPLICATE KEY UPDATE {update_data_key};'
#     return sql_insert, data_value
#
#
# def get_sql_select_id(data, table_name):
#     query_fields = ["package_name", "lj_package_id", "version", "package_version", "dependency_package_name",
#                     "dependency_package_version"]
#     sql_list = []
#     for each in query_fields:
#         if each in data.keys():
#             if data[each] is None:
#                 sql_list.append(f'{each} is null')
#             else:
#                 sql_list.append(f'{each} = "{data[each]}"')
#     sql_query = ' and '.join(sql_list)
#     sql_select_id = f"select id from {table_name} where {sql_query}"
#     return sql_select_id


# def get_increment_sql(increment_data, table_name, increment_id, is_insert):
#     datas = increment_data.items()
#     insert_data_key = ','.join([x[0] for x in datas])
#     data_value = [x[1] for x in datas]
#     num_s = ('%s,' * len(increment_data))[:-1]
#     sql_increment = f"insert into {table_name} (id,is_insert,time,{insert_data_key}) VALUES({increment_id},{is_insert},curdate(),{num_s})"
#     return sql_increment, data_value


# def data_to_db(insert_data, conn, table_name, increment_fields):
#     '''
#     :param table_info: 表的连接、数据库、表名信息
#     :param insert_data: 插入的数据，字典形式-->{'字段名':值}
#     :param incre_table_info: 增量表的连接、数据库、表名信息
#     :param increment_fields: ["lj_package_id", "package_name", "home_page", "first_release_time", "latest_release_time",
#                     "latest_release", "description", "language", "keywords", "license", "verified_license"]
#                     ["package_name","lj_package_id","version","published_time","license","verified_license"]
#                     ["lj_package_id","package_version","dependency_package_name","dependency_package_version"]
#     :return:
#     '''
#     conn.ping(reconnect=True)
#     increment_table_name = table_name + '_increment'
#     increment_data = {}
#     for each in increment_fields:
#         increment_data[each] = insert_data[each]
#     sql_insert, data_value = get_insert_sql(insert_data, table_name)
#     with conn.cursor() as cursor:
#         is_insert = cursor.execute(sql_insert, data_value * 2)  # 返回值为1，该记录不存在，插入了数据；返回值为2，该记录存在，并且更新了数据
#         if is_insert != 0:
#             sql_select_id = get_sql_select_id(insert_data, table_name)
#             cursor.execute(sql_select_id)
#             increment_id = cursor.fetchone()[0]
#             sql_increment, data_value = get_increment_sql(increment_data, increment_table_name, increment_id, is_insert)
#             cursor.execute(sql_increment, data_value)
#     # conn.commit()
#     return is_insert


class Cargo_dep:
    def __init__(self):
        client = pymongo.MongoClient(MONGO_CLIENT)
        db = client['Cargo']
        collection_info_versions = db['Cargo_info_versions']
        self.collection_dep = db['Cargo_dep']
        self.lj_id = pymysql.connect(host=MYSQL_17_HOST,
                                     port=MYSQL_17_PORT,
                                     user=MYSQL_17_USER,
                                     password=MYSQL_17_PASSWORD,
                                     db=MYSQL_17_DB,
                                     charset=MYSQL_17_CHARSET,
                                     cursorclass=pymysql.cursors.DictCursor)
        self.xx = pymysql.connect(host=MYSQL_HOST,
                                  port=MYSQL_PORT,
                                  user=MYSQL_USER,
                                  password=MYSQL_PASSWORD,
                                  db=MYSQL_DB,
                                  charset=MYSQL_CHARSET)
        self.mysql_queue_conn = pymysql.connect(host=MYSQL_QUEUE_HOST,
                                                port=MYSQL_QUEUE_PORT,
                                                user=MYSQL_QUEUE_USER,
                                                password=MYSQL_QUEUE_PASSWORD,
                                                db=MYSQL_QUEUE_DB,
                                                charset=MYSQL_QUEUE_CHARSET,
                                                cursorclass=pymysql.cursors.DictCursor)

    # def get_lj_package_id(self, package_path):
    #     with self.lj_id.cursor(pymysql.cursors.DictCursor) as cursor_package_id:
    #         # 获取lj_package_id
    #         package_name = package_path
    #         # 3、从sql表info中拿出相应的数据拿出package_id，project_id
    #         sql = '''SELECT id,project_id FROM lj_id_map_package where package_name = '{}' and type = "cargo"'''.format(
    #             package_name)
    #         cursor_package_id.execute(sql)  # 传入表名也就是包管理器类型
    #         data = cursor_package_id.fetchone()
    #         if not data:
    #             with self.mysql_queue_conn.cursor(pymysql.cursors.DictCursor) as cursor_queue:
    #                 sql = "insert ignore into package_spider_queue.cargo_spider_queue(package_name) values ('%s')" % (
    #                     package_name)
    #                 cursor_queue.execute(sql)
    #                 self.mysql_queue_conn.commit()
    #             self._map_lj_id_one(package_name)
    #             with self.lj_id.cursor(pymysql.cursors.DictCursor) as cursor:
    #                 sql = "SELECT id,project_id FROM lj_id.lj_id_map_package where package_name = '{}' and type = 'cargo'".format(
    #                     package_name)
    #                 cursor.execute(sql)
    #                 data = cursor.fetchone()
    #         if not data:
    #             lj_id = None
    #             # self.logger.error("{} 的 {} 包 lj_package_id 生成异常".format(package_type, package_name))
    #         else:
    #             # self.logger.info("{} 的 {} 包 lj_package_id 生成成功".format(package_type, package_name))
    #             lj_id = data['id']
    #         return lj_id

    # def _map_lj_id_one(self, package_name):
    #     sql = "insert ignore into lj_id.lj_id_map_package (package_name, type) values ('{}', 'cargo')".format(
    #         package_name)
    #     with self.lj_id.cursor(pymysql.cursors.DictCursor) as cursor:
    #         cursor.execute(sql)
    #         self.lj_id.commit()

    # def Insert_sql_data(self, data):
    #     '''
    #
    #     :param table_info: 表的连接、数据库、表名信息
    #     :param insert_data: 插入的数据，字典形式-->{'字段名':值}
    #     :param incre_table_info: 增量表的连接、数据库、表名信息
    #     :return:
    #     '''
    #     conn = data.get('conn')
    #     table = data.get('table')
    #     insert_data = data.get('insert_data')
    #     datas = insert_data.items()
    #     insert_data_name = ','.join([x[0] for x in datas])
    #     data_value = [x[1] for x in datas]
    #     num_s = ('%s,' * len(insert_data))[:-1]
    #     update_data_name = ','.join([x[0] + '=%s' for x in datas])
    #     sql = 'INSERT INTO `{}`({}) VALUES({}) ON DUPLICATE KEY UPDATE {};'.format(table, insert_data_name, num_s,
    #                                                                                update_data_name)
    #     # print(sql%tuple((data_value * 2)))
    #     with conn as cursor:
    #         res = cursor.execute(sql, data_value * 2)  # 返回值为1，该记录不存在，插入了数据；返回值为2，该记录存在，并且更新了数据
    #     # print('{} 插入成功'.format(insert_data.get('lj_package_id')))

    def get_result(self, package_name):
        for result in self.collection_dep.find({'id': package_name}):
            yield result

    def main(self, package_name, package_type):
        increment_fields = 'package_name,dependency_lj_package_id,dependency_kind,lj_package_id,package_version,dependency_package_name,dependency_package_version'.split(
            ',')
        for result in self.get_result(package_name):
            package_name = result.get('id')
            package_version = result.get('verson')
            for dependency in result.get('dependencies', []):
                dependency_kind = dependency.get('kind')
                if dependency_kind != 'dev':
                    dependency_package_name = dependency.get('crate_id')
                    dependency_package_version = dependency.get('req').replace('^', '')
                    table_name = 'cargo_spider_queue'
                    lj_package_id = LjIdClass().get_lj_package_id(package_name, package_type, table_name)
                    # lj_package_id = self.get_lj_package_id(package_name, package_type, table_name)
                    dependency_lj_package_id = LjIdClass().get_lj_package_id(dependency_package_name, package_type,
                                                                             table_name)
                    # dependency_lj_package_id = self.get_lj_package_id(dependency_package_name)
                    compare_str = package_name + package_version + dependency_kind + dependency_package_name + dependency_package_version
                    md5 = hashlib.md5()
                    md5.update(compare_str.encode("utf8"))
                    compare_md5 = md5.hexdigest()
                    insert_data = {"lj_package_id": lj_package_id, 'package_version': package_version,
                                   'dependency_package_name': dependency_package_name,
                                   "dependency_package_version": dependency_package_version,
                                   'package_name': package_name,
                                   'dependency_lj_package_id': dependency_lj_package_id,
                                   'dependency_kind': None,
                                   'compare_md5': compare_md5}
                    log_data = {
                        'log_type': '入库',
                        'to_table': f'{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}/cargo_package_dependencies',
                        'data_content': {
                            'package_name': package_name,
                            'package_version': package_version,
                            'package_type': 'cargo'
                        },
                        'data_status': None
                    }
                    try:
                        dep_mes = PackageDeps(package_name, package_type, dependency_package_version,
                                              dependency_type='', requirement=[])
                        is_insert = insert_to_db_tool.package_version(dep_mes)
                        # is_insert = data_to_db(insert_data, self.xx, 'cargo_package_dependencies', increment_fields)
                        if is_insert == 1:
                            log_data['data_status'] = '新增'
                        elif is_insert == 2:
                            log_data['data_status'] = '更新'
                        if is_insert != 0:
                            logger.info(f'{package_name} 入库成功', extra=log_data)
                    except Exception as e:
                        logger.error(f'{package_name} 入库失败，{e}', extra=log_data)
                    # print(insert_data)
            self.xx.commit()
            self.collection_dep.update({'_id': result.get('_id')}, {'$set': {"is_insert": 1}})


def dep_main(package_name, package_type):
    # Cargo_dep().main(package_name)
    Cargo_dep().main(package_name, package_type)
