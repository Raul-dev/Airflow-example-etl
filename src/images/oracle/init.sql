
alter session set container=XEPDB1
create user dbo
alter user dbo identified by password
create schema dbo AUTHORIZATION dbo
grant create any table to dbo
grant dba to dbo
CREATE TABLE dbo.TABLE0(
    id number
);