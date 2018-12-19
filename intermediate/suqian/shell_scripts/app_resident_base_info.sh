#!/bin/bash

cur_date=`date +%Y-%m`
echo $cur_date
month=${cur_date:5:2}
if [ $((month%2)) -eq 0 ];then
    echo "0"

hive -e "
        insert overwrite table adm_test.app_resident_base_info

        select 

        coalesce(resident_name,'')                     ,
        coalesce(resident_id_type,'')                  ,
        coalesce(resident_id,'')                       ,
        coalesce(birth_date,'')                        ,
        coalesce(resident_sex,'')                      ,
        coalesce(resident_type,'')                     ,
        coalesce(house_number,'')                      ,
        coalesce(relat_2_landlord,'')                  ,
        coalesce(census_register,'')                   ,
        regexp_replace(regexp_replace(contact_info,'\\\\\\\\',''),'\\\\\\\\','') as contact_info ,
        coalesce(habitant_address,'')                  ,
        coalesce(address_match_status,'')              ,
        coalesce(trans.property_right_certificate_number,'') as property_right_certificate ,
        '暂无'criminal_info                     ,
        regexp_replace(regexp_replace(company_info,'\\\\\\\\',''),'\\\\\\\\','') as company_info ,
        coalesce(company_address,'')            ,
        current_timestamp create_time           ,
        current_timestamp update_time           ,
        1 as data_flag                          ,
        coalesce(people.pro_coll_id,'')         ,    ---房屋id
        coalesce(ori.officer_no,'')  ---警员编号        

        from (
            select 
            resident_name,
            resident_id_type,
            resident_id,
            birth_date,
            resident_sex,
            resident_type,
            house_number,
            relat_2_landlord,
            case when odm_perm.pro_coll_id is not null then concat( pro_coll_xiaoqu, pro_coll_qu, pro_coll_zhuang, pro_coll_danyuan ,pro_coll_fanghao) else xz end as census_register ,
            coalesce(contact_info,'') as contact_info,
            case when odm_perm.pro_coll_id is not null then concat( pro_coll_xiaoqu, pro_coll_qu, pro_coll_zhuang, pro_coll_danyuan ,pro_coll_fanghao) else xz end as habitant_address , 
            case when odm_perm.pro_coll_id is not null then 1 else 0 end as address_match_status ,
            coalesce(company_info,'') as company_info,
            company_address,
            odm_perm.pro_coll_id,
            pro_coll_xiaoqu
            
            
            
            from (
                    select iidd,
                         xm resident_name ,
                        '身份证' resident_id_type ,
                        sfzhm resident_id ,
                        csrq  birth_date ,
                        xb resident_sex  ,  
                        '常住人口' resident_type,
                        hh  house_number ,
                        YHZGX relat_2_landlord,
                        lxdh contact_info,
                        xz,
                        fwcs   company_info , ---暂且认为是公司名称 
                        '不详' company_address
                    from  bdm_test.bdm_za_ck_czrk_jbxx where ssxq = 321311 ) czrk
                    left join odm_test.odm_pro_coll_and_permanent_residence odm_perm ---房产与常住人口数据中间表
                    on odm_perm.permanent_residence_id = czrk.iidd

                    union all
                    select     ---暂住人口 
                         
                        resident_name,
                        resident_id_type,
                        resident_id,
                        birth_date,
                        resident_sex,
                        resident_type,
                        house_number,
                        relat_2_landlord,
                        census_register ,
                        contact_info,
                        case when odm_temp.pro_coll_id is not null then concat( pro_coll_xiaoqu, pro_coll_qu, pro_coll_zhuang, pro_coll_danyuan ,pro_coll_fanghao) else ZZDZBC end as habitant_address , 
                        case when odm_temp.pro_coll_id is not null then 1 else 0 end as address_match_status ,
                        company_info,
                        company_address,
                        odm_temp.pro_coll_id,
                        pro_coll_xiaoqu
                    
                    from (
                             select iidd,
                                 xm resident_name ,
                                '身份证' resident_id_type ,
                                JMZH  resident_id ,
                                csrq birth_date ,
                                xb resident_sex  ,  
                                '暂住人口' resident_type,
                                hh house_number ,
                                HZGX relat_2_landlord,
                                GRLXDH contact_info ,
                                DWDZ company_address ,
                                HJDZXZ  census_register ,
                                ZZDZBC,
                                fwcs company_info
                            from  bdm_test.bdm_za_jzz_zzrk_sj where xzqh = 321311 ) zzrk
                    left join odm_test.odm_pro_coll_and_temporary_residence odm_temp
                    on zzrk.iidd = odm_temp.temporary_residence_id
        ) people
        left join 
        (
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
                   
                   ) pctr
        on people.pro_coll_id =pctr.pro_coll_id
        left join (select * from  
                        (select * , row_number() over(partition by property_address,property_apartment_num,property_house_num order by property_issue_date desc , property_area desc ,property_area desc ) as row_num from  
                        bdm_test.bdm_real_estate_transaction 
                        where property_source != '自建' and property_apartment_num not like '%商铺%' and property_name not like '%房地产开发%' 
                        and property_address not like '%门面%' and property_apartment_num not like '%门面%' and property_house_num not like '%储藏%') t 
                        where t.row_num = 1 
         ) trans 
        on pctr.house_deal_id = trans.property_right_certificate_number 
        left join bdm_test.bdm_community_officer_relationshop_info ori
        on people.pro_coll_xiaoqu = ori.community_name 
        where resident_name !='' and resident_id !=''
        ;

"
else 
   echo '1'
fi 
