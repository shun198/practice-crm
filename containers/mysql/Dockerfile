FROM mysql:8.0

# MySQLのローカルの設定ファイルをコンテナにコピー
COPY containers/mysql/my.cnf /etc/mysql/conf.d/my.cnf
# init.sqlをコンテナの/docker-entrypoint-init.db.dと共有
COPY containers/mysql/init.sql /docker-entrypoint-initdb.d