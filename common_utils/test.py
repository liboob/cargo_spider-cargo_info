from package.lj_sqlpackage import *
from retry import retry

insert_to_db_tool = SqlTool(host='mysql.center.spdx.cn', port=3306, user='data_center', pwd='52KIXFwbh4zG', db='data_center',
                            charset='utf8mb4')
# @retry(stop_max_delay=20)
def test():
    # version_mes = PackageVersion('absperf-minilzo-sys', 'cargo', '0.1.3', 'GPL-2.444', '2020-05-21', 'GPL-2.444')
    # insert = insert_to_db_tool.package_version(version_mes)
    # print(insert)

    info_mes =  PackageVersion('abstract-ref' 'cargo' '0.1.0-alpha.1' 'MIT OR Apache-2.0' '2021-01-14' 'MIT')
    insert = insert_to_db_tool.package_info(info_mes)
    print(insert)
if __name__ == '__main__':
    test()
# file = PackageFile(1, 2, 123, 123, 123, 123)
# print(sqltoolsa.package_file(file))


# # info = PackageInfo(11, 22, 33, 44, 55, 66)
# # sql.package_info(info)


# info = PackageInfo('LOL', 2, 36, 4, 5, 6)
# print(sqltoolsa.package_info(info))

# version = PackageVersion('1.2.31', 'pbce许', '2022-06-26', 'LOL', '6')
# print(sqltoolsa.package_version(version))
#
# dep = {'httpoison': {'app': 'LOL', 'optional': False, 'requirement': '~> 0.9.0'},
#        'poison': {'app': 'LOL', 'optional': False, 'requirement': '~> 2.2'}}
# dep = [{'app': 'LOL', 'optional': False, 'requirement': '~> 0.9.0'}, {'app': 'LOL', 'optional': False, 'requirement': '~> 2.2'}]
# deps = PackageDeps( 'LOL', '6', '1', '6', dep)
# print(sqltoolsa.package_deps(deps))


#
# # version = PackageVersion(2,3,datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'),1,6)
# # sql.package_version(version)
#
# # file = PackageFile(1, 2, 3, 4, 5, 6)
# # sql.package_file(file)
#
# dep = PackageDeps(1, 2, 3, 4, 5, 6, 7, 8)
# sql.package_deps(dep)
#
# dep = {'httpoison': {'app': '11', 'optional': False, 'requirement': '~> 0.9.0'}, 'poison': {'app': '11', 'optional': False, 'requirement': '~> 2.2'}}
# deps = PackageDeps('~> 0.9.0','1', '3', '11', '5', '6', '66', dep)
# # sqltoolsa = SqlTool()
# print(sql.package_deps(deps))
