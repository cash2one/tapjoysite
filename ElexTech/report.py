#!/usr/bin/env python

import xlwt, os, sys, datetime
import config
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

def main():
    settings = config.SQL_CONFIG
    connection = get_connection(dsn = 'VerticaDSN', unicode_results='True')
    cursor = connection.cursor()
    try:
        cursor.execute('select year(CURRENT_DATE - 2), month(CURRENT_DATE - 2), day(CURRENT_DATE - 2 )')
        rows = cursor.fetchall()
        month = '{0:4d}{1:02d}'.format(rows[0].year, rows[0].month);
        day = '{0:4d}{1:02d}{2:02d}'.format(rows[0].year, rows[0].month, rows[0].day)

	BASEDIR = os.path.join(os.path.realpath(sys.path[0]), 'report')
        
        folder = os.path.join(BASEDIR, month)
        filename = os.path.join(BASEDIR, month, day) + '.xls'
        
	if not os.path.exists(folder):
            os.mkdir(folder)	
       
        wb = xlwt.Workbook()
        for setting in settings:
            print str(datetime.datetime.now()) + '''  Pull data for "%s" ... ''' % setting['name']
            cursor.execute(setting['sql'])
            #print setting['sql']
            AddSheet(wb, setting['name'], cursor, setting['row'], setting['col'])
 
        wb.save(filename)

    except Exception as ex:
        print str(datetime.datetime.now()) + '''  Pull data for "%s" failed''' % setting['name']
        print Exception, ":", ex

    finally:
        connection.close()



if __name__ == "__main__":
    main()

