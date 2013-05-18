SQL_CONFIG =\
[\

    {'name':'ad spend',\
     'sql':'''select par.offer_name, ctr.country_name, count(*), sum(convs.advertiser_amount*-0.01)
              from analytics.conversions convs  
              join mstr.country_dimension ctr on ctr.country_iso3661_code=convs.country
              join analytics.offers_partners par on convs.advertiser_offer_id=par.offer_id
              where par.partner_id='51bd38ac-b226-4ad7-a566-992b0ab862e3' and date(convs.created_at)=CURRENT_DATE-2
              group by 1,2 
              order by 1,2,3 DESC''', \
      'row':0, \
      'col':0,
    }, \



]



     


