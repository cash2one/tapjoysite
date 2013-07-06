#!/usr/bin/env python

import xlwt, os, sys, datetime
from pyvertica.connection import get_connection


def AddSheet(wb, sheet, cr, mac_format, orig_row = 0, orig_col = 0):
    rows = cr.fetchall()
    #print len(rows)
    ws0 = wb.add_sheet(sheet)

    row_num = orig_row 
    column_num = orig_col

    for cell in rows[0].cursor_description:
        ws0.write(row_num, column_num, cell[0])
        column_num += 1

    row_num = +1
    format_dict = {
            '1': lambda f: f,
            '2': lambda f: f.upper(),
            '3': lambda f: ''.join([ f[i] + ':' if i % 2 else f[i] for i in range(len(f)) ]).strip(':'),
            '4': lambda f: ''.join([ f[i] + ':' if i % 2 else f[i] for i in range(len(f)) ]).strip(':').upper(),
        }
    
    for row in rows:
        ws0.write(row_num, orig_col, row[0])
        ws0.write(row_num, orig_col + 1, format_dict[mac_format](str(row[1])))
        row_num += 1

def generateReport(adID, startDate, endDate, macFormat, queryID = 'tmp'):
    connection = get_connection(dsn = 'VerticaDSN', unicode_results='True')
    cursor = connection.cursor()
    try:
        BASEDIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tmp_report')
        folder =  BASEDIR
        filename = os.path.join(BASEDIR, queryID) + '.xls'

	if not os.path.exists(folder):
            os.mkdir(folder)	

        wb = xlwt.Workbook()
        print str(datetime.datetime.now()) + '''  Pull data for offer "%s" ... ''' % adID 
        sql = ''' select distinct to_char(a.time + interval '8:00') as clicktime, b.mac_address  
                  from (select udid, time from analytics.actions where offer_id = '%s' 
                  and time between date('%s') - interval '8:00' and date('%s') + interval '16:00') a 
                  join analytics.connects_bi b on a.udid = b.udid
                  where b.mac_address != 'NULL' and b.day between date('%s') - interval '15' and '%s'
                  order by 1 asc''' % (adID, startDate, endDate, startDate, endDate)
        #print sql
        cursor.execute(sql)
        #cursor.execute('''select '12123' as clicktime, 'abc12' as mac_addr''')
        AddSheet(wb, 'mac_addr', cursor, macFormat, 0, 0)
        wb.save(filename)



    except Exception as ex:
        print str(datetime.datetime.now()) + '''  Failed to pull data for offer "%s" ... ''' % adID 
        print Exception, ":", ex
    finally:
        connection.close()


if __name__ == "__main__":
    generateReport('2bdabb67-0406-435e-871a-dd8fd6ce786e', '2013-6-25', '2013-6-28', '1', 'tmp')

