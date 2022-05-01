#安装docker
sudo yum install -y yum-utils
sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo docker run hello-world
sudo groupadd docker
sudo usermod -aG docker $USER

#安装mysql client
wget http://repo.mysql.com/mysql80-community-release-el7-1.noarch.rpm
sudo rpm -ivh mysql80-community-release-el7-1.noarch.rpm
rpm --import https://repo.mysql.com/RPM-GPG-KEY-mysql-2022
yum install mysql-community-client

#配置git
cd ~/.ssh
ssh-keygen
cat id_rsa.pub #配置到自己的git仓库
yum install git

#下载代码
cd /opt/
git clone git@github.com:kellyxiepei/django_bootstrap.git #换成自己的仓库地址

#Build镜像
cd django_bootstrap/
docker build -t "django_bootstrap:v1_0" -f ./deploy/Dockerfile .

