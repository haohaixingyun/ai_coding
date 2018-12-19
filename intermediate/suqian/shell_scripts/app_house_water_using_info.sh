#!/bin/bash

cur_date=`date +%Y-%m`
pre_date=`date -d "-2 month" +%Y-%m`
min_12_month=`date -d "-12 month" +%Y-%m`

if [[ $# == 0 ]];then 
echo $0
elif [[ $# == 1 ]];then
echo $1
cur_date=`date -d $1 +%Y-%m`
pre_date=`date -d "$1 -2 month" +%Y-%m`
min_12_month=`date -d "$1 -12 month" +%Y-%m`
fi 
echo "the current date",$cur_date
echo "the previous date",$pre_date
echo "the previous year",$min_12_month


month=${cur_date:5:2}
if [ $((10#$month%2)) -eq 0 ];then

    echo "0"

hive -e "
        insert overwrite table tmp.app_house_water_using_info partition(dt = '"""$cur_date"""')

        select 
		coalesce(pc.pro_coll_id,'')                  ,  --房屋主键
        coalesce(pc.community_name,'')               , 
        coalesce(pc.community_district,'')           ,
        coalesce(pc.apartment_num,'')                ,           
        coalesce(pc.house_unit,'')                   ,              
        coalesce(pc.room_num,'')                     ,                 
        case when co_temp.temporary_residence_id is not null then '出租'     	---2代表出租
             when co_perm.permanent_residence_id is not null then '自住'     	---1代表自住
             when coalesce(current_period_water_qty,0) = 0 then '空置'       ---已销售空置房
                 else '待核' end  house_status,                                  ---0代表待核
        coalesce(trans.property_name, regist.buyer_name)  landlord_name         ,            
        coalesce(trans.id_number, regist.buyer_id)  landlord_id                 ,       
        coalesce(trans_phone.lxdh , regist_phone.lxdh) landlord_phone           ,          
        coalesce(previous_period_water_qty,0) as previous_water_consumption ,
        coalesce(current_period_water_qty,0) as  current_water_consumption  ,
        coalesce(water_avg,0) as avg_water_consumption                                                          ,
        coalesce(current_period_water_qty,0) /coalesce(previous_period_water_qty,1)  month_on_month_growth                        ,
        coalesce(water_stddev,0)/(case when water_avg = 0 then 1 else coalesce(water_avg,1) end ) coefficient_variation   ,  
        abs(coalesce(current_period_water_qty,0) - coalesce(water_avg_sc,0))/(case when water_stddev_sc = 0 then 1 else coalesce(water_stddev_sc,1) end ) as standard_score   ,           
        coalesce(cor.officer_no,'') ,        
        CURRENT_TIMESTAMP as judge_abnormal_time   ,     
        '' as house_water_status ,    ---1 代表正常 ，如果是异常 0    
        CURRENT_TIMESTAMP as create_time    ,            
        CURRENT_TIMESTAMP as update_time                

        from 
        odm_test.odm_property_collection_table pc   ----
        left join odm_test.odm_pro_coll_and_registration odm_regist    
        on pc.pro_coll_id = odm_regist.pro_coll_id
        left join 
        (select * from 
                                ( select * , row_number() over(partition by commercial_housing_contract_number order by building_area desc ) row_num
                                 from bdm_test.bdm_real_estate_registration  )t  where t.row_num = 1  ) regist  --房产登记信息 
        on odm_regist.house_register_id =regist.commercial_housing_contract_number  
        left join (
		   select * from (
		   select odm_trans.*,row_number() over(partition by property_address,property_apartment_num,property_house_num order by property_issue_date desc ) rw_num from  odm_test.odm_pro_coll_and_transaction odm_trans 
           inner join 
		   (select * from  
                        (select * , row_number() over(partition by property_right_certificate_number order by property_issue_date desc , property_area desc ,property_area desc ) as row_num from  
                        bdm_test.bdm_real_estate_transaction 
                        where property_source != '自建' and property_apartment_num not like '%商铺%' and property_name not like '%房地产开发%'
						and property_address not like '%门面%' and property_apartment_num not like '%门面%' and property_house_num not like '%储藏%') t 
                        where t.row_num = 1 
         ) trans 
		 on 
		   odm_trans.house_deal_id = trans.property_right_certificate_number 
		   
        		) t where t.rw_num =1   
				   
				   )odm_trans
        on pc.pro_coll_id = odm_trans.pro_coll_id
        left join 
        (select * from  
                        (select * , row_number() over(partition by property_address,property_apartment_num,property_house_num order by property_issue_date desc , property_area desc ,property_area desc ) as row_num from  
                        bdm_test.bdm_real_estate_transaction 
                        where property_source != '自建' and property_apartment_num not like '%商铺%' and property_name not like '%房地产开发%' 
						and property_address not like '%门面%' and property_apartment_num not like '%门面%' and property_house_num not like '%储藏%') t 
                        where t.row_num = 1 
         ) trans 
        on odm_trans.house_deal_id = trans.property_right_certificate_number 
        left join (select distinct water_id ,pro_coll_id ,water_xiaoqu, water_qu,water_zhuang,water_danyuan,water_fanghao ,pro_coll_xiaoqu,pro_coll_qu,pro_coll_zhuang,pro_coll_danyuan,pro_coll_fanghao from odm_test.odm_pro_coll_and_tap_water ) odm_water
        on pc.pro_coll_id = odm_water.pro_coll_id
        left join 
        (select stddev(current_period_water_qty) water_stddev,avg(current_period_water_qty)   water_avg , customer_num from bdm_test.bdm_tap_water_information_collection where dt >='"""$min_12_month"""'   and water_type like '%居民生活%'  group by customer_num) maths---取最近一次的数据，以及近一年的方差，四分位数据，变异系数，平均月用水量)
        on odm_water.water_id = maths.customer_num
        left join (select customer_num ,current_period_water_qty from bdm_test.bdm_tap_water_information_collection where dt  = '"""$cur_date"""' and water_type like '%居民生活%') cur  ---这个月水量
        on odm_water.water_id = cur.customer_num
        left join (select customer_num ,current_period_water_qty as previous_period_water_qty from bdm_test.bdm_tap_water_information_collection where dt  = '"""$pre_date"""' and water_type like '%居民生活%' ) pre   ---上月水量
    on odm_water.water_id = pre.customer_num
        left join (select * from ( select * ,row_number() over(partition by sfzhm order by updatetime , lxdh) row_num from  bdm_test.bdm_za_ck_czrk_jbxx ) t where row_num =1 )  trans_phone ---链接人口获取联系电话
        on trans.id_number  =  trans_phone.sfzhm
    left join (select * from ( select * ,row_number() over(partition by sfzhm order by updatetime , lxdh) row_num from bdm_test.bdm_za_ck_czrk_jbxx ) t where row_num =1 ) regist_phone  ---链接人口获取联系电话
        on regist.buyer_id = regist_phone.sfzhm
        left join 
        (select stddev(current_period_water_qty) water_stddev_sc,avg(current_period_water_qty)  water_avg_sc  ,customer_num from bdm_test.bdm_tap_water_information_collection where dt >='"""$min_12_month"""' and dt <= '"""$pre_date"""'  and water_type like '%居民生活%'  group by customer_num) maths_sc ---取最近一次的数据，以及近一年的方差，四分位数据，变异系数，平均月用水量)
        on odm_water.water_id = maths_sc.customer_num
        inner join bdm_test.bdm_community_officer_relationshop_info cor
        on pc.community_name = cor.community_name
        left join(select * from (select *,row_number() over(partition by pro_coll_id order by permanent_residence_id) rw_num from odm_test.odm_pro_coll_and_permanent_residence) t where rw_num =1 ) co_perm   ----需要去重
        on pc.pro_coll_id = co_perm.pro_coll_id
        left join (select * from (select *,row_number() over(partition by pro_coll_id order by temporary_residence_id) rw_num from odm_test.odm_pro_coll_and_temporary_residence ) t where rw_num =1) co_temp   ----需要去重
        on pc.pro_coll_id = co_temp.pro_coll_id

"
else 
   echo '1'

fi  