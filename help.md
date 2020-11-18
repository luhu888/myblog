linux（centeros）安装Python3.6

 yum install python36

## Linux（centos） 上安装 MySQL

Linux平台上推荐使用RPM包来安装Mysql,MySQL AB提供了以下RPM包的下载地址：

- **MySQL** - MySQL服务器。你需要该选项，除非你只想连接运行在另一台机器上的MySQL服务器。
- **MySQL-client** - MySQL 客户端程序，用于连接并操作Mysql服务器。
- **MySQL-devel** - 库和包含文件，如果你想要编译其它MySQL客户端，例如Perl模块，则需要安装该RPM包。
- **MySQL-shared** - 该软件包包含某些语言和应用程序需要动态装载的共享库(libmysqlclient.so*)，使用MySQL。
- **MySQL-bench** - MySQL数据库服务器的基准和性能测试工具。

安装前，我们可以检测系统是否自带安装 MySQL:

```
rpm -qa | grep mysql
```

如果你系统有安装，那可以选择进行卸载:

```markdown
rpm -e mysql　　// 普通删除模式
rpm -e --nodeps mysql　　// 强力删除模式，如果使用上面命令删除时，提示有依赖的其它文件，则用该命令可以对其进行强力删除
```

```
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm
rpm -ivh mysql-community-release-el7-5.noarch.rpm
yum update  # 查看到需要安装的软件，输入n，不必全部安装
yum install mysql-server
```

权限设置：

```
chown mysql:mysql -R /var/lib/mysql
```

初始化 MySQL：

```
mysqld --initialize
```

启动 MySQL：

```
systemctl start mysqld
```

查看 MySQL 运行状态：

```
systemctl status mysqld
```

**注意：**如果我们是第一次启动 mysql 服务，mysql 服务器首先会进行初始化的配置。

添加MySQL root 密码

```
mysql -u root
SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpass');
```

安装git

```
yum -y install git
ssh-keygen -t rsa -C "luhu0105@gmail.com"
cat  /root/.ssh/id_rsa.pub
```

linux目录简介

```
/opt目录用来安装附加软件包，它所有的数据、库文件等等都是放在同个目录下面。当你不需要时，直接rm -rf掉即可。
/usr：系统级的目录，可以理解为C:/Windows/。
/usr/lib：理解为C:/Windows/System32。
/usr/local：用户级的程序目录，可以理解为C:/Progrem Files/。用户自己编译的软件默认会安装到这个目录下。
usr/src：系统级的源码目录。
/usr/local/src：用户级的源码目录
```

安装指定版本Python虚拟环境

```
sudo pip3 install virtualenv
which python3
virtualenv -p /usr/bin/python3  env_name
source env_name/bin/activate  #开启虚拟环境
deactivate  # 退出虚拟环境
```

部署django项目

```
开启虚拟环境后操作
git clone git@github.com:luhu888/myblog.git
pip3 install -r requirements.txt 
create database myblog default character set 'utf8';
python manage.py makemigrations
python manage.py makemigrations blog
没有生成对应表可以在后面加应用名
python manage.py migrate
delete from django_migrations where app='user';
修改model后migrate没有自动修改对应表的字段，删除migrations中app记录，以及admin记录
使用重写之后的user表迁移数据要先迁移new_user表，否则会报错admin_log表已存在
可以使用 python manage.py migrate --fake admin 重置migration解决
python manage.py createsuperuser
/opt/env_list/env_myblog/lib/python3.6/site-packages/django/forms/boundfield.py", line 93,
注释掉虚拟环境中Django的93行
python manage.py runsever 127.0.0.1:8005
STATIC_ROOT = os.path.join(BASE_DIR,'static')  # settings中添加，用于存放后台的静态资源
python manage.py collectstatic  # 将静态资源拷过来
yum install -y gcc* pcre-devel openssl-devel  装nginx也需要这个
yum search python3-devel
yum install python3-devel.x86_64
pip3 install uwsgi（上面3个yum为安装uwsgi的编译工具）
安装nginx
wget http://nginx.org/download/nginx-1.13.7.tar.gz
mv nginx-1.13.7.tar.gz /home/   将下载错位置的压缩包移到home文件夹下
cd nginx-1.13.7
./configure
make
make install

nginx一般默认安装好的路径为/usr/local/nginx
在/usr/local/nginx/conf/中先备份一下nginx.conf文件，以防意外。
cp nginx.conf nginx.conf.bak
然后打开nginx.conf，把原来的内容删除，直接加入以下内容：
worker_processes  1;
events {
    worker_connections  1024;
}
http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    server {
        listen       80;
        server_name  182.92.120.140;
        charset utf-8;
        location / {
           include uwsgi_params;
           uwsgi_pass 127.0.0.1:8001;
           uwsgi_param UWSGI_SCRIPT /opt/project/myblog/myblog/wsgi.py;
           uwsgi_param UWSGI_CHDIR /opt/project/myblog/myblog;
           
        }
        location /static/ {
        alias /opt/project/myblog/static/;
        }
    }
}
进入/usr/local/nginx/sbin/目录
执行./nginx -t命令先检查配置文件是否有错，没有错就执行以下命令：
./nginx
ln -s /usr/local/nginx/sbin/nginx  /usr/local/bin
使用软连接，全局使用nginx命令
在/etc/init.d/ 文件夹下创建nginx文件，输入以下内容：
#!/bin/bash
#
# chkconfig: - 85 15
# description: Nginx is a World Wide Web server.
# processname: nginx

nginx=/usr/local/nginx/sbin/nginx
conf=/usr/local/nginx/conf/nginx.conf
case $1 in
start)
echo -n "Starting Nginx"
$nginx -c $conf
echo " done"
;;
stop)
echo -n "Stopping Nginx"
killall -9 nginx
echo " done"
;;
test)
$nginx -t -c $conf
;;
reload)
echo -n "Reloading Nginx"
ps auxww | grep nginx | grep master | awk '{print $2}' | xargs kill -HUP
echo " done"
;;
restart)
$0 stop
$0 start
;;
show)
ps -aux|grep nginx
;;
*)
echo -n "Usage: $0 {start|restart|reload|stop|test|show}"
;;
esac
注意使用unix换行符
yum install -y dos2unix
dos2unix /etc/init.d/nginx
sudo chmod +x /etc/init.d/nginx  # 更改文件权限
chkconfig --add /etc/init.d/nginx # 将nginx添加至chkconfig管理列表
chkconfig --level 2345 nginx on   # 用chkconfig设置其开机启动
systemctl daemon-reload  # 告诉系统重新加载下新添加的文件，然后就可以全局使用nginx命令了
在Django项目根目录下创建mysite.ini
[uwsgi]
socket = 127.0.0.1:8001
chdir = /opt/project/myblog/
wsgi-file = /opt/project/myblog/myblog/wsgi.py
processes = 4
threads = 2
stats = 127.0.0.1:9191
netstat -anp |grep 8001
sudo kill -9 17590   # 查看占用端口并解除占用
fuser -k 8001/tcp   # 强杀端口相关进程
uwsgi -d --ini /opt/project/myblog/mysite.ini
修改代码同步到服务器需要将uwsgi进程杀掉重启，否则代码无法及时更新
killall -9 uwsgi


GRANT ALL PRIVILEGES ON *.* TO 用户@"%" IDENTIFIED BY "密码";
flush privileges;
mysql设置允许远程登录，同时注意修改阿里云安全组规则

scp -r D:\Users\hulu\PycharmProjects\myblog-master\mysite.ini root@182.92.120.144:/opt/
将本地文件传到服务器上
```

