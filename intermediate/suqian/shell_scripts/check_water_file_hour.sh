#!/bin/bash


if [[ $# == 0 ]];then 
echo $0
elif [[ $# == 1 ]];then
echo $1
cur_date=`date -d $1 +%Y-%m`
pre_date=`date -d "$1 -2 month" +%Y-%m`
min_12_month=`date -d "$1 -12 month" +%Y-%m`
fi 

time=`date +%Y%m%d%H%M%S`
echo 'echo the time: ',$time

echo "the current date",$cur_date
echo "the previous date",$pre_date
echo "the previous year",$min_12_month


month=${cur_date:5:2}

## need to define the water file path ,the owner must put it in a fixed path with fixed style

waterFile='../waterfile.txt'
waterFlagdone='../waterflag.txt'

if [ -f "$waterFile" ];then
    
	echo "water file existed will check if the date is a even number"
	if [ $((10#$month%2)) -eq 0 ];then

		echo "the date time is a even number will load water file into hive database "
		echo "start load water file into hive db"
		hive -e "select 1"
		echo "end load water file into hive db"
		
		echo "start to backup the water file..."
		mv $waterFile $waterFile$time
		echo "end to backup the water file ..."
		if [ ! -f "$waterFlagdone" ];then
			touch "$waterFlagdone"
		fi 
		
	else 
	   echo "the date time is a odd number will NOT load water file into hive database "

	fi  
else
  echo 'file not existed'
fi