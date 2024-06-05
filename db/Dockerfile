FROM mysql/mysql-server:latest

# Copy necessary data from the upgrade stage (if applicable)
COPY --from=upgrader /var/lib/mysql /var/lib/mysql

# Set the root password for MySQL (change 'aODIJfe3' to your desired password)
ENV MYSQL_ROOT_PASSWORD=aODIJfe3

# Set the MySQL database name
ENV MYSQL_DATABASE=financedata

# Set the MySQL password for the 'root' user
ENV MYSQL_PASSWORD=aODIJfe3

# Expose the MySQL port
EXPOSE 3306

# COPY config/user.cnf /etc/mysql/my.cnf
# Mount a volume for persistent data storage
VOLUME /var/lib/mysql

