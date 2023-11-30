# conda create -n database_PJ python=3.8
# conda activate database_PJ
pip install -r requirements.txt


mysql -u root -p
# enter your root password

CREATE USER 'DB_admin'@'localhost' IDENTIFIED BY 'DB_admin';
CREATE DATABASE DB_PJ;
GRANT ALL PRIVILEGES ON DB_PJ.* TO 'DB_admin'@'localhost';
FLUSH PRIVILEGES;
EXIT;

mysql -u DB_admin -p
# enter your DB_admin password
