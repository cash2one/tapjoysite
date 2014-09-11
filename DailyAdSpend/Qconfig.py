SQL_CONFIG =\
   { 

        'quarter':'2014Q3',
        'days': 92,
        'offset': 1, 
        'sql': '''select date(convs.created_at), off_par.sales_rep_email as SR, par_mgr.acct_mgr as AM, sum(convs.advertiser_amount*-0.01)
		 from analytics.conversions convs 
		 join analytics.offers_partners off_par on convs.advertiser_offer_id= off_par.offer_id
		 join analytics.partner_acct_mgr par_mgr on par_mgr.partner_id = off_par.partner_id
		 where date(convs.created_at) = CURRENT_DATE-%d and 
		      (par_mgr.acct_mgr in
			('adams.ma@tapjoy.com','heping.yu@tapjoy.com','huabing.zhu@tapjoy.com','max.wang@tapjoy.com',
			 'ming.wang@tapjoy.com','sandy.shen@tapjoy.com','tyler.zhang@tapjoy.com','wang.rui@tapjoy.com','wendy.mao@tapjoy.com',
			 'xiaosi.gao@tapjoy.com','yameng.zhang@tapjoy.com','zhihui.cai@tapjoy.com') 
		     or 
		      off_par.sales_rep_email in
			('adams.ma.dev@tapjoy.com','adams.ma@tapjoy.com','david.chun@tapjoy.com','heping.yu@tapjoy.com','ming.wang@tapjoy.com',
			 'rae.wang.dev@tapjoy.com','sandy.shen@tapjoy.com','tyler.zhang@tapjoy.com','wang.rui@tapjoy.com','wendy.mao@tapjoy.com',
			 'xiaosi.gao@tapjoy.com','yameng.zhang@tapjoy.com','zhihui.cai@tapjoy.com'))
		 group by 1, 2, 3 
		 order by 4 desc''',

         'maillist': ['david.chun@tapjoy.com', 
		'adams.ma@tapjoy.com', 
		'xiaosi.gao@tapjoy.com', 
		'huabing.zhu@tapjoy.com',
		'ming.wang@tapjoy.com',
		'wang.rui@tapjoy.com',
		'zhihui.cai@tapjoy.com',
		'tyler.zhang@tapjoy.com',
		'cathy.fan@tapjoy.com',
		'mabel.zhao@tapjoy.com',
		'max.wang@tapjoy.com',
		'wendy.mao@tapjoy.com',
		'sandy.shen@tapjoy.com',
		'michelle.ao@tapjoy.com',
		'yameng.zhang@tapjoy.com',
		'heping.yu@tapjoy.com',
		'song.peng@tapjoy.com',
		'li.zhe@tapjoy.com', ],
         'owner': 
         {
		'ming.wang@tapjoy.com-yameng.zhang@tapjoy.com':'Mingming',
		'david.chun@tapjoy.com-ming.wang@tapjoy.com':'Mingming',
		'david.chun@tapjoy.com-zhihui.cai@tapjoy.com':'Zhihui',
		'zhihui.cai@tapjoy.com-zhihui.cai@tapjoy.com':'Zhihui',
		'zhihui.cai@tapjoy.com-heping.yu@tapjoy.com':'Zhihui',
		'tyler.zhang@tapjoy.com-tyler.zhang@tapjoy.com':'Tyler',
		'xiaosi.gao@tapjoy.com-tyler.zhang@tapjoy.com':'Tyler', 
		'tyler.zhang@tapjoy.com-sandy.shen@tapjoy.com':'Tyler', 
		'xiaosi.gao@tapjoy.com-heping.yu@tapjoy.com':'xiaosi',
		'xiaosi.gao@tapjoy.com-wendy.mao@tapjoy.com':'xiaosi',
		'xiaosi.gao@tapjoy.com-xiaosi.gao@tapjoy.com':'xiaosi',
		'adams.ma@tapjoy.com-adams.ma@tapjoy.com':'Adams',
		'adams.ma@tapjoy.com-huabing.zhu@tapjoy.com':'Huabing',
		'adams.ma@tapjoy.com-max.wang@tapjoy.com':'Max',
		'wang.rui@tapjoy.com-wang.rui@tapjoy.com':'Rae',
		'wang.rui@tapjoy.com-wendy.mao@tapjoy.com':'Wendy',
		'david.chun@tapjoy.com-wendy.mao@tapjoy.com':'Wendy',
		'wendy.mao@tapjoy.com-wendy.mao@tapjoy.com':'Wendy',
		'wang.rui@tapjoy.com-sandy.shen@tapjoy.com':'Sandy',
		'xiaosi.gao@tapjoy.com-sandy.shen@tapjoy.com':'Sandy',
		'heping.yu@tapjoy.com-heping.yu@tapjoy.com':'Heping',
                'adams.ma@tapjoy.com-hetty.yu@tapjoy.com':'Heping',
		'wang.rui@tapjoy.com-heping.yu@tapjoy.com':'Heping',
		'yameng.zhang@tapjoy.com-yameng.zhang@tapjoy.com':'Yameng',
		'sandy.shen@tapjoy.com-sandy.shen@tapjoy.com':'Internal',
                'rae.wang.dev@tapjoy.com-justin.im@tapjoy.com':'Zhihui',
		'adams.ma.dev@tapjoy.com-huabing.zhu@tapjoy.com':'Huabing',
		'rae.wang.dev@tapjoy.com-wendy.mao@tapjoy.com':'Wendy',
		'rae.wang.dev@tapjoy.com-wang.rui@tapjoy.com':'Rae',
		'rae.wang.dev@tapjoy.com-wang.rui@tapjoy.com':'Rae',
         },
         'kpi':
         {
                'Mingming':1450000,
		'Zhihui':2590000,
		'Tyler':580000,
		'xiaosi':520000,
		'Adams':547000,
		'Huabing':563000,
		'Max':90000,
		'Rae':290000,
		'Wendy':370000,
		'Sandy':310000,
		'Heping':247000,
		'Yameng':74000,
                'Internal': 0
         }


   }  
