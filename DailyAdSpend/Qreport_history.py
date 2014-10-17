#!/usr/bin/env python

#-*-coding:utf8-*-
import xlwt
import os
import sys
import datetime
import Qconfig
import pyodbc
import json
from pyvertica.connection import get_connection




def main():
    settings = Qconfig.SQL_CONFIG
    #connection = get_connection(dsn='VerticaDSN', unicode_results='True')
    connection = pyodbc.connect("DSN=VerticaDSN")
    cursor = connection.cursor()

    mailjobs = {}
    day = ''
    partner = 'China'
    alldays = 84
    try:

        cursor.execute(
            'select year(CURRENT_DATE - %d), month(CURRENT_DATE - %d), day(CURRENT_DATE - %d )' % (alldays, alldays, alldays))
        rows = cursor.fetchall()
        month = '{0:4d}{1:02d}'.format(rows[0].year, rows[0].month)
        day = '{0:4d}{1:02d}{2:02d}'.format(
            rows[0].year, rows[0].month, rows[0].day)
        print day
        

        BASEDIR = os.path.join(os.path.realpath(sys.path[0]), 'Qreport')
        folder = os.path.join(BASEDIR, partner, month)
        jsonfile = os.path.join(BASEDIR, partner , settings['quarter']) + '.json'

        if not os.path.exists(folder):
            os.makedirs(folder)
 
        #if os.path.exists(jsonfile):
        #    f = file(jsonfile)
        #    spend_data = json.load(f)
        #    f.close()
        #else:
        #    spend_data = {};
        spend_data = {}
	sqltmp = '''select date(convs.created_at), off_par.sales_rep_email as SR, par_mgr.acct_mgr as AM, sum(convs.advertiser_amount*-0.01)
                 from analytics.conversions convs 
                 join analytics.offers_partners off_par on convs.advertiser_offer_id= off_par.offer_id
                 join analytics.partner_acct_mgr par_mgr on par_mgr.partner_id = off_par.partner_id
                 where date(convs.created_at) = CURRENT_DATE- %d and 
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
                 order by 4 desc'''
        
        for i in xrange(alldays, 1, -1):
            print i
            cursor.execute(sqltmp % i)
            rows = cursor.fetchall()
            daydata = {}
            for row in rows:
                key = row[1] + '-' + row[2];
                daydata[key] = (float(row[3]))
            spend_data[row[0].strftime('%Y-%m-%d')] = daydata 
            
        #print json.dumps(spend_data, indent=4)
        json.dump(spend_data, open(jsonfile, 'w'))

    except Exception as ex:
        print str(datetime.datetime.now()) + '''  Pull data for "%s" failed''' % partner 
        print Exception, ":", ex

    finally:
        connection.close()




if __name__ == "__main__":
    main()
