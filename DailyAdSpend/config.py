SQL_CONFIG =\
    [

        {'name': 'ad spend',
         'sql': '''select par.offer_name, app.app_platform, ctr.country_name, count(*), sum(convs.advertiser_amount*-0.01)
              from analytics.conversions convs
              join mstr.country_dimension ctr on ctr.country_iso3661_code=convs.country
              join analytics.offers_partners par on convs.advertiser_offer_id=par.offer_id
              join analytics.apps_partners app on convs.publisher_app_id=app.app_id
              where par.partner_id='51bd38ac-b226-4ad7-a566-992b0ab862e3' and date(convs.created_at)=CURRENT_DATE-2
              group by 1,2,3
              order by 1,2,3,4 DESC''',
         'row': 0,
         'col': 0,
         'partnername': 'Elex',
         'maillist': ["song.peng@tapjoy.com", 'ming.wang@tapjoy.com', 'wendy.mao@tapjoy.com', 'rae.wang@tapjoy.com']
         },

        {'name': 'ad spend',
         'sql': '''select par.offer_name, app.app_platform, ctr.country_name, count(*), sum(convs.advertiser_amount*-0.01)
              from analytics.conversions convs
              join mstr.country_dimension ctr on ctr.country_iso3661_code=convs.country
              join analytics.offers_partners par on convs.advertiser_offer_id=par.offer_id
              join analytics.apps_partners app on convs.publisher_app_id=app.app_id
              where par.partner_id='da250978-05f3-438d-9414-fa2347e2284a' and date(convs.created_at)=CURRENT_DATE-2
              group by 1,2,3
              order by 1,2,3,4 DESC''',
         'row': 0,
         'col': 0,
         'partnername': 'WOODTALE',
         'maillist': ["song.peng@tapjoy.com", 'ming.wang@tapjoy.com', 'wendy.mao@tapjoy.com', 'rae.wang@tapjoy.com'],
         },

        {'name': 'ad spend',
         'sql': '''select par.offer_name, app.app_platform, ctr.country_name, count(*), sum(convs.advertiser_amount*-0.01)
              from analytics.conversions convs
              join mstr.country_dimension ctr on ctr.country_iso3661_code=convs.country
              join analytics.offers_partners par on convs.advertiser_offer_id=par.offer_id
              join analytics.apps_partners app on convs.publisher_app_id=app.app_id
              where par.partner_id='bd86e697-97d5-4f60-a4e2-38c246a9746c' and date(convs.created_at)=CURRENT_DATE-2
              group by 1,2,3
              order by 1,2,3,4 DESC''',
         'row': 0,
         'col': 0,
         'partnername': 'Efun1',
         'maillist': ['ming.wang@tapjoy.com']
         },

        {'name': 'ad spend',
         'sql': '''select par.offer_name, app.app_platform, ctr.country_name, count(*), sum(convs.advertiser_amount*-0.01)
              from analytics.conversions convs
              join mstr.country_dimension ctr on ctr.country_iso3661_code=convs.country
              join analytics.offers_partners par on convs.advertiser_offer_id=par.offer_id
              join analytics.apps_partners app on convs.publisher_app_id=app.app_id
              where par.partner_id='350cb434-e6f8-4cf8-94f8-34f13781cb93' and date(convs.created_at)=CURRENT_DATE-2
              group by 1,2,3
              order by 1,2,3,4 DESC''',
         'row': 0,
         'col': 0,
         'partnername': 'Efun2',
         'maillist': ['ming.wang@tapjoy.com']
         },

        {'name': 'ad spend',
         'sql': '''select par.offer_name, app.app_platform, ctr.country_name, count(*), sum(convs.advertiser_amount*-0.01)
              from analytics.conversions convs
              join mstr.country_dimension ctr on ctr.country_iso3661_code=convs.country
              join analytics.offers_partners par on convs.advertiser_offer_id=par.offer_id
              join analytics.apps_partners app on convs.publisher_app_id=app.app_id
              where par.partner_id='3a9f6bb8-c840-4b48-994f-8ef00927693f' and date(convs.created_at)=CURRENT_DATE-2
              group by 1,2,3
              order by 1,2,3,4 DESC''',
         'row': 0,
         'col': 0,
         'partnername': 'Efun3',
         'maillist': ['ming.wang@tapjoy.com']
         },

    ]
