# Use an official MySQL image from the Docker Hub
FROM mysql/mysql-server:8.0.33

# Set the root password for MySQL (change 'aODIJfe3' to your desired password)
ENV MYSQL_ROOT_PASSWORD=aODIJfe3

# Set the MySQL database name
ENV MYSQL_DATABASE=financedata

# Set the MySQL password for the 'root' user
ENV MYSQL_PASSWORD=aODIJfe3

# Expose the MySQL port
EXPOSE 3306

COPY config/user.cnf /etc/mysql/my.cnf
# Mount a volume for persistent data storage
VOLUME /var/lib/mysql

