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


import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

#MAIL_LIST = ["song.peng@tapjoy.com", 'ming.wang@tapjoy.com']
MAIL_FROM = 'Peng Song' + "<" + 'song.peng' + "@" + 'tapjoy.com.cn' + ">"


def send_mail(subject, content, mailjobs=None):
    try:

        smtp = smtplib.SMTP()
        smtp.connect()

        for (filename, maillist) in mailjobs.items():
            if filename != None and os.path.exists(filename):
                message = MIMEMultipart()
                message.attach(MIMEText(content))
                message["Subject"] = subject
                message["From"] = MAIL_FROM
                message["To"] = ";".join(maillist)
                ctype, encoding = mimetypes.guess_type(filename)
                if ctype is None or encoding is not None:
                    ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1)
                attachment = MIMEImage((lambda f: (f.read(), f.close()))(
                    open(filename, "rb"))[0], _subtype=subtype)
                attachment.add_header(
                    "Content-Disposition", "attachment", filename=os.path.split(filename)[-1])
                message.attach(attachment)

                smtp.sendmail(MAIL_FROM, maillist, message.as_string())

        smtp.quit()

        return True
    except Exception, errmsg:
        print "Send mail failed to: %s" % errmsg
        return False


def addSheetAmount(wb, spend_data):
    settings = Qconfig.SQL_CONFIG 
    ws0 = wb.add_sheet('amount') 
    
    days = spend_data.keys()
    days.sort();
    
    dat = {};
    for owner, kpi in settings['kpi'].items():
        dat[owner] = {};
        dat[owner]['QKPI'] = kpi
        dat[owner]['DKPI'] = float(kpi) / settings['days']
        dat[owner]['QtD'] = 0
    
    for i in xrange(0, len(days)):
        daydata = spend_data[days[i]]
        for key, value in daydata.items():
            owner = settings['owner'][key]
            dat[owner]['QtD'] += value;
            dat[owner][i] = value + dat[owner].get(i,0);
    row = 0
    col = 0

    ws0.write(row, col, 'Owner')
    col += 1
    ws0.write(row, col, 'Percent')
    col += 1
    ws0.write(row, col, 'QKPI')    
    col += 1
    ws0.write(row, col, 'QtD')    
    col += 1
    ws0.write(row, col, 'DKPI')    
    col += 1
    for i in xrange(len(days), 0, -1):
         ws0.write(row, col, days[i-1]) 
         col += 1
        
    iter = dat.items()
    sum = 'Total'
    dat[sum] = {};
    dat[sum]['QKPI'] = 0
    dat[sum]['DKPI'] = 0
    dat[sum]['QtD'] = 0
   
    for owner, value in iter:
        row += 1 
        col = 0
        ws0.write(row, col, owner)
        col += 1
        if owner == 'Internal':
            ws0.write(row, col, 0)
        else:
            ws0.write(row, col, '%.2f%%' % (value['QtD']/ value['QKPI'] * 100))
        col += 1
        
        ws0.write(row, col, value['QKPI'])
        dat[sum]['QKPI'] += value['QKPI'];
        col += 1
        ws0.write(row, col, value['QtD'])
        dat[sum]['QtD'] += value['QtD'];
        col += 1
        ws0.write(row, col, value['DKPI'])
        dat[sum]['DKPI'] += value['DKPI'];
        col += 1
        for i in xrange(len(days), 0, -1): 
            ws0.write(row, col, value.get(i-1, 0))  
            dat[sum][i-1] = value.get(i-1, 0) + dat[sum].get(i-1, 0)
            col += 1
   
    row += 2
    col = 0
    ws0.write(row, col, 'Total')
    col += 1
    ws0.write(row, col, '%.2f%%' % (dat[sum]['QtD']/ dat[sum]['QKPI'] * 100))
    col += 1
    ws0.write(row, col, dat[sum]['QKPI'])
    col += 1
    ws0.write(row, col, dat[sum]['QtD'])
    col += 1
    ws0.write(row, col, dat[sum]['DKPI'])
    col += 1
    for i in xrange(len(days), 0, -1):
            ws0.write(row, col, dat[sum].get(i-1, 0)) 
            col += 1
   
        

 

    

def AddSheet(wb, sheet, cr, orig_row=0, orig_col=0):
    rows = cr.fetchall()
    if len(rows) < 1:  # no record
        return False
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

    return True


def main():
    settings = Qconfig.SQL_CONFIG
    connection = pyodbc.connect("DSN=VerticaDSN")
    cursor = connection.cursor()

    mailjobs = {}
    day = ''
    partner = 'China'
    try:
        cursor.execute(
            'select year(CURRENT_DATE - %d), month(CURRENT_DATE - %d), day(CURRENT_DATE - %d )' % 
            (settings['offset'], settings['offset'], settings['offset']) )
        rows = cursor.fetchall()
        month = '{0:4d}{1:02d}'.format(rows[0].year, rows[0].month)
        day = '{0:4d}{1:02d}{2:02d}'.format(
            rows[0].year, rows[0].month, rows[0].day)

        BASEDIR = os.path.join(os.path.realpath(sys.path[0]), 'Qreport')
        folder = os.path.join(BASEDIR, partner, month)
        filename = os.path.join(BASEDIR, partner , month, partner + '_' + day) + '.xls'
        jsonfile = os.path.join(BASEDIR, partner , settings['quarter']) + '.json'

        if not os.path.exists(folder):
            os.makedirs(folder)

        wb = xlwt.Workbook()

 
        if os.path.exists(jsonfile):
            f = file(jsonfile)
            spend_data = json.load(f)
            f.close()
        else:
            spend_data = {};
        cursor.execute(settings['sql'] % settings['offset'])
        rows = cursor.fetchall()
        daydata = {}
        for row in rows:
           key = row[1] + '-' + row[2];
           daydata[key] = (float(row[3]))
        spend_data[row[0].strftime('%Y-%m-%d')] = daydata 
#       #print json.dumps(spend_data, indent=4)
        json.dump(spend_data, open(jsonfile, 'w'))

        addSheetAmount(wb, spend_data);
            #if AddSheet(wb, period, cursor, sqlset['row'], sqlset['col']):

        wb.save(filename)
        mailjobs[filename] = settings['maillist']
    except Exception as ex:
        print str(datetime.datetime.now()) + '''  Pull data for "%s" failed''' % partner 
        print Exception, ":", ex

    finally:
        connection.close()

    subject = 'TeamChina ' + settings['quarter'] + ' QtD adspend report'

    send_mail(subject, 'Please find the visualized version at http://www.tapjoy.cn:8765/adspend/china/. \n\n\n This is a daily report by Tapjoy.cn\n\n', mailjobs)


if __name__ == "__main__":
    main()
