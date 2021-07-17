use mysql;
-- new user
set password for root@localhost = password('123456');
-- important
grant all on *.* to root@'%' identified by '123456' with grant option;
-- use privileges
flush privileges;