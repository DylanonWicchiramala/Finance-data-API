cd .\app
python -m prepare_database

timeout /t 3
scp -r .\app\data\financedata.db srv-cpk1i56d3nmc73fn9d30@ssh.oregon.render.com:/var/lib/data