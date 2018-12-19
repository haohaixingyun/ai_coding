hive -e "
insert overwrite table adm_test.APP_RESIDENT_BASE_INFO_test

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
        regexp_replace(regexp_replace(contact_info,'\\',''),'\\','') as contact_info ,
        coalesce(habitant_address,'')                  ,
        coalesce(address_match_status,'')              ,
        coalesce(property_right_certificate,'') as property_right_certificate ,
        '暂无'criminal_info                     ,
        regexp_replace(regexp_replace(company_info,'\\',''),'\\','') as company_info ,
        coalesce(company_address,'')            ,
        current_timestamp create_time           ,
        current_timestamp update_time           ,
        1 as data_flag                          ,
        coalesce(pro_coll_id,'')         ,    ---房屋id
        coalesce(officer_no,'')  ---警员编号     
       from     ADM_TEST.APP_RESIDENT_BASE_INFO where resident_id in ( 320819196309082426 ,370123200003241011)    "