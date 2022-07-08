# coding=utf-8
import pymysql
import pymongo
import requests

from common_utils.common_methods import *
from common_utils.env_settings import *

logger = LoggerClass('python-package', 'cargo', is_print=1)

from package.lj_sqlpackage import *

insert_to_db_tool = SqlTool(host='mysql.center.spdx.cn', port=3306, user='data_center', pwd='52KIXFwbh4zG', db='data_center',
                            charset='utf8mb4')


def license_key(document):
    # jar_path = os.path.join(os.path.abspath('.'), r'extract-1.0-SNAPSHOT-jar-with-dependencies.jar')
    #
    # if not jpype.isJVMStarted():
    #     jpype.startJVM('-ea', classpath=jar_path)
    # if document:
    #     HanLP = JClass('com.ljqc.license_copyright.extract.utils.Extract')
    #     key = HanLP.extractLicenseByContent(document)
    #     if key:
    #         return key
    #     else:
    #         return None
    # else:
    #     return None
    try:
        headers = {
            'Content-Type': 'text/plain'
        }
        res = requests.post(LICENSE_URL, data=document, headers=headers)
        return res.text
    except:
        return ''


# def get_insert_sql(insert_data, table_name):
#     datas = insert_data.items()
#     insert_data_key = ','.join([x[0] for x in datas])
#     data_value = [x[1] for x in datas]
#     num_s = ('%s,' * len(insert_data))[:-1]
#     update_data_key = ','.join([x[0] + '=%s' for x in datas])
#     sql_insert = f'INSERT INTO `{table_name}`({insert_data_key}) VALUES({num_s}) ON DUPLICATE KEY UPDATE {update_data_key};'
#     return sql_insert, data_value

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

#
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
#     conn.commit()
#     return is_insert

class Cargo:
    def __init__(self):
        # 创建sql连接
        # self.conn_xx = pymysql.connect(host=MYSQL_HOST,
        #                                port=MYSQL_PORT,
        #                                user=MYSQL_USER,
        #                                password=MYSQL_PASSWORD,
        #                                db=MYSQL_DB,
        #                                charset=MYSQL_CHARSET)

        # self.license = pymysql.connect(host='192.168.31.17',
        #                                port=3306,
        #                                user='root',
        #                                password='ti9#aN%^^ToqacQD',
        #                                db='dataVerify',
        #                                charset='utf8')

        # self.lj_id = pymysql.connect(host=MYSQL_17_HOST,
        #                              port=MYSQL_17_PORT,
        #                              user=MYSQL_17_USER,
        #                              password=MYSQL_17_PASSWORD,
        #                              db=MYSQL_17_DB,
        #                              charset=MYSQL_17_CHARSET,
        #                              cursorclass=pymysql.cursors.DictCursor)
        # self.mysql_queue_conn = pymysql.connect(host=MYSQL_QUEUE_HOST,
        #                                         port=MYSQL_QUEUE_PORT,
        #                                         user=MYSQL_QUEUE_USER,
        #                                         password=MYSQL_QUEUE_PASSWORD,
        #                                         db=MYSQL_QUEUE_DB,
        #                                         charset=MYSQL_QUEUE_CHARSET,
        #                                         cursorclass=pymysql.cursors.DictCursor)

        client = pymongo.MongoClient(MONGO_CLIENT)  # 117数据库链接
        db = client['Cargo']
        self.collection = db['Cargo_info_versions']

    # def verify_license(self, license):
    #     if license:
    #         process_license = license.replace('-', ' ')
    #         process_license = process_license.replace('–', ' ')
    #         process_license = process_license.replace("'", '')
    #         process_license = process_license.replace('"', '')
    #         process_license = process_license.replace("#", '')
    #         process_license = process_license.replace('~', ' ')
    #         process_license = process_license.replace('(', '').replace(')', '').replace('[', '').replace(']', '')
    #         process_license = process_license.strip()  # 去掉左右空格
    #         process_license = process_license.lower()  # 转全小写
    #         process_license = ' '.join([x for x in process_license.split(' ') if x])  # 多个空格间隔变成一个间隔
    #         # 传入包管理器类型，license
    #         sql_license = 'SELECT verify_license FROM `license_verify` WHERE verify_license  is not null and origin_license = "{}"'.format(
    #             process_license)
    #         with self.license.cursor(pymysql.cursors.DictCursor) as c:
    #             c.execute(sql_license)
    #             license_data = c.fetchone()
    #             if license_data:
    #                 return license_data.get('verify_license').strip()
    #             else:
    #                 return
    #     else:
    #         return

    # def insert_sql_data(self, data):
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
    #     conn.commit()
    #     print('{}插入完成'.format(insert_data.get('package_name')))

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

    def get_results(self, package_name):
        # for result in self.collection.find({'is_insert': {'$exists': False}}):
        for result in self.collection.find({'id': package_name}):
            # print(result)
            # # input()
            # print(">>>>>>>>>>>>>>>>>>>")
            yield result

    # 主流程
    def cargo_main(self, package_name, package_type):
        for result in self.get_results(package_name):
            package_name = result.get('id')
            # table_name = 'cargo_spider_queue'
            # lj_package_id = LjIdClass().get_lj_package_id(package_name, package_type, table_name)
            # package_url = 'https://crates.io/crates/{}'.format(package_name)
            # versions_count = len(result.get('versions'))
            home_page = result.get('homepage')
            github_url = result.get('repository')
            # latest_release_time = result.get('updated_at')[:10]
            latest_release = result.get('max_version')
            description = result.get('description')
            versions = result.get('versions')
            info_license = ''
            # license_key = versions.get('license')
            # print(license_key)



            # version信息处理并入库
            for version_results in versions:
                license = version_results.get('license')
                version = version_results.get('num')
                published_time = version_results.get('created_at')[:10]
                # download_url = 'https://crates.io{}'.format(version_results.get('dl_path'))
                if version == latest_release:
                    info_license = license
                # ver_license = self.verify_license(license)
                # ver_license = license_key(license) if license else ''
                # log_data = {
                #     'log_type': '清洗',
                #     'handle_from_table': f'{MONGO_HOST}:{MYSQL_PORT}/Cargo/Cargo_info_versions',
                #     'handle_to_table': f'{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}/cargo_package_versions',
                #     'handle_from_field': 'license',
                #     'handle_to_field': 'verified_license',
                #     'handle_from_value': license,
                #     # 'handle_to_value': ver_license,
                #     'data_content': {
                #         'package_name': package_name,
                #         'package_version': version,
                #         'package_type': 'cargo'
                #     }
                # }
                # if not ver_license:
                #     ver_license = license
                #     logger.error(f'字段:{log_data["handle_from_field"]} 清洗失败', extra=log_data)

                # insert_data_version = {"package_name": package_name, 'version': version,
                #                        "published_time": published_time, 'license': license,
                #                        "download_url": download_url,
                #                        'lj_package_id': lj_package_id,
                #                        'verified_license': ver_license
                #                        }
                # version_str = 'package_name,lj_package_id,version,version,published_time,license,verified_license'.split(
                #     ',')
                log_data = {
                    'log_type': '入库',
                    'data_content': {
                        'package_name': package_name,
                        'package_version': version,
                        'package_type': 'cargo'
                    },
                    'data_status': None
                }
                # version信息入库
                try:
                    version_mes = PackageVersion(package_name, package_type, version, published_time, info_license)
                    print(package_name, package_type, version, info_license, published_time)
                    is_insert = insert_to_db_tool.package_version(version_mes)
                    # print(is_insert)
                    # is_insert = data_to_db(insert_data_version, self.conn_xx, 'cargo_package_versions', version_str)
                    if is_insert == 1:
                        log_data['data_status'] = '新增'
                    elif is_insert == 2:
                        log_data['data_status'] = '更新'
                    if is_insert != 0:
                        logger.info(f'{package_name} 入库成功', extra=log_data)
                except Exception as e:
                    logger.error(f'{package_name} 入库失败，{e}', extra=log_data)

            # insert_data_info = {'versions_count': versions_count,
            #                     'package_name': package_name, 'latest_release_time': latest_release_time,
            #                     'description': description, 'latest_release': latest_release, 'home_page': home_page,
            #                     'license': info_license, 'lj_package_id': lj_package_id,
            #                     'github_url': github_url,
            #                     'verified_license': license_key(info_license) if info_license else ''
            #                     }
            # info_str = 'lj_package_id,package_name,home_page,latest_release_time,latest_release,description,license,verified_license'.split(
            #     ',')
            # info信息入库
            log_data = {
                'log_type': '入库',
                'data_content': {
                    'package_name': package_name,
                    'package_version': None,
                    'package_type': 'cargo'
                },
                'data_status': None
            }
            try:
                print("info的信息如下：")
                print(package_name, package_type, description, home_page, github_url, info_license)
                info_mes = PackageInfo(package_name, package_type, info_license, description, home_page, github_url)
                is_insert = insert_to_db_tool.package_info(info_mes)
                # is_insert = data_to_db(insert_data_info, self.conn_xx, 'cargo_packages_info', info_str)
                # print(insert_data_info)
                if is_insert == 1:
                    log_data['data_status'] = '新增'
                elif is_insert == 2:
                    log_data['data_status'] = '更新'
                if is_insert != 0:
                    logger.info(f'{package_name} 入库成功', extra=log_data)
                self.collection.update({'_id': result.get('_id')}, {'$set': {"is_insert": 1}})
            except Exception as e:
                logger.error(f'{package_name} 入库失败，{e}', extra=log_data)


def info_main(package_name, package_type):
    Cargo().cargo_main(package_name, package_type)
