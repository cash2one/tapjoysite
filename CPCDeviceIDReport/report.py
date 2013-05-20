#!/usr/bin/env python

import xlwt, os, sys, datetime
from pyvertica.connection import get_connection


def AddSheet(wb, sheet, cr, orig_row = 0, orig_col = 0):
    rows = cr.fetchall()
    ws0 = wb.add_sheet(sheet)

    row_num = orig_row 
    column_num = orig_col

    for cell in rows[0].cursor_description:
        ws0.write(row_num, column_num, cell[0])
        column_num += 1

    row_num = +1
    for row in rows:
        column_num = orig_col 
        for cell in row:
            ws0.write(row_num, column_num, cell)
            column_num += 1
        row_num += 1

def generateReport(adID, startDate, endDate, queryID = 'tmp'):
    connection = get_connection(dsn = 'VerticaDSN', unicode_results='True')
    cursor = connection.cursor()
    try:
        BASEDIR = os.path.join(os.path.realpath(sys.path[0]), 'CPCDeviceIDReport', 'tmp_report')
        folder =  BASEDIR
        filename = os.path.join(BASEDIR, queryID) + '.xls'

	if not os.path.exists(folder):
            os.mkdir(folder)	

        wb = xlwt.Workbook()
        print str(datetime.datetime.now()) + '''  Pull data for offer "%s" ... ''' % adID 
        sql = ''' select distinct to_char(a.time + interval '8:00') as clicktime, b.mac_address  
                  from (select udid, time from analytics.actions where offer_id = '%s' 
                  and day between '%s' and '%s') a 
                  join analytics.connects_bi b on a.udid = b.udid
                  where b.mac_address != 'NULL' and b.day between date('%s') - interval '15' and '%s'
                  order by 1 asc
                 ''' % (adID, startDate, endDate, startDate, endDate)
        cursor.execute(sql)
        AddSheet(wb, 'mac_addr', cursor, 0, 0)
        wb.save(filename)
    except:
        print str(datetime.datetime.now()) + '''  Failed to pull data for offer "%s" ... ''' % adID 
    finally:
        connection.close()


if __name__ == "__main__":
    generateReport('03da3e55-bf5d-4057-9278-36915429a2ff', '2013-5-1', '2013-5-3', 'tmp')

