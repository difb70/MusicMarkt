need to configure the file database_cfg.py, with the following information : 
- **username**, **password** : that correspond to the created credentials on the RDBMS, that allow the remote connection to the musicmarkt database
```python
DB_HOST = "192.168.1.1"
DB_USER = "<username>"
DB_PASSWORD = "<password>"
DB_DATABASE = "musicmarkt"
DB_CONNECTION_STRING = f"host={DB_HOST} dbname={DB_DATABASE} user={DB_USER} password={DB_PASSWORD}"
```
