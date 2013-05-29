SQL_CONFIG =\
[\

    {'name':'ad spend',\
     'sql':'''select par.offer_name, app.app_platform, ctr.country_name, count(*), sum(convs.advertiser_amount*-0.01)
              from analytics.conversions convs  
              join mstr.country_dimension ctr on ctr.country_iso3661_code=convs.country
              join analytics.offers_partners par on convs.advertiser_offer_id=par.offer_id
              join analytics.apps_partners app on convs.publisher_app_id=app.app_id
              where par.partner_id='402c2767-f90b-4596-b35c-c40f83137e31' and date(convs.created_at)=CURRENT_DATE-2
              group by 1,2,3 
              order by 1,2,3,4 DESC''', \
      'row':0, \
      'col':0,
    }, \



]



     


