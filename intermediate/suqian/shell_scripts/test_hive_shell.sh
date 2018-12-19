#!/bin/bash

hive -e "


use odm;
drop table test_hive_job;
create table test_hive_job(

name string comment 'your name'

);
insert into  test_hive_job values('ethan_Sharon');



"
