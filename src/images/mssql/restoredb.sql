IF(DB_ID(N'DBPlatform') IS NULL)
RESTORE DATABASE DBPlatform FROM DISK = '/var/opt/mybackup/dbplatform.bak' 
WITH MOVE 'DBPlatform' TO '/var/opt/mssql/data/dbplatform.mdf', 
MOVE 'DBPlatform_log' TO '/var/opt/mssql/data/dbplatform_log.ldf'