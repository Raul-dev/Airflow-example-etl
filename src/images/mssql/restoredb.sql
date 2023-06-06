IF(DB_ID(N'DBPlatform') IS NULL)
RESTORE DATABASE DBPlatform FROM DISK = '/var/opt/mybackup/DBPlatform.bak' 
WITH MOVE 'DBPlatform' TO '/var/opt/mssql/data/DBPlatform.mdf', 
MOVE 'DBPlatform_log' TO '/var/opt/mssql/data/DBPlatform_log.ldf'