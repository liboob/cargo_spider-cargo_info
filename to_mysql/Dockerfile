FROM registry.cn-beijing.aliyuncs.com/ctu_scrapy/mypython:3.1

WORKDIR /usr/src

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

COPY . .

CMD ["python", "cargo_mysql/mysql_run.py"]

