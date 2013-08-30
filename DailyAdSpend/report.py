#!/usr/bin/env python

#-*-coding:utf8-*- 
import xlwt, os, sys, datetime
import config
from pyvertica.connection import get_connection



import  smtplib, mimetypes 
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.multipart import MIMEMultipart 

MAIL_LIST = ["song.peng@tapjoy.com", 'ming.wang@tapjoy.com'] 
MAIL_FROM = 'Penguin' + "<"+ 'song.peng' + "@" + 'tapjoy.com.cn' + ">"

def send_mail(subject, content, files = None): 
    try: 
        message = MIMEMultipart() 
        message.attach(MIMEText(content)) 
        message["Subject"] = subject 
        message["From"] = MAIL_FROM 
        message["To"] = ";".join(MAIL_LIST) 
        for filename in files:
            if filename != None and os.path.exists(filename): 
                ctype, encoding = mimetypes.guess_type(filename) 
                if ctype is None or encoding is not None: 
                    ctype = "application/octet-stream"
                maintype, subtype = ctype.split("/", 1) 
                attachment = MIMEImage((lambda f: (f.read(), f.close()))(open(filename, "rb"))[0], _subtype = subtype) 
                attachment.add_header("Content-Disposition", "attachment", filename = os.path.split(filename)[-1]) 
                message.attach(attachment) 

        smtp = smtplib.SMTP() 
        smtp.connect() 
        smtp.sendmail(MAIL_FROM, MAIL_LIST, message.as_string()) 
        smtp.quit() 

        return True
    except Exception, errmsg: 
        print "Send mail failed to: %s" % errmsg 
        return False


def AddSheet(wb, sheet, cr, orig_row = 0, orig_col = 0):
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
    settings = config.SQL_CONFIG
    connection = get_connection(dsn = 'VerticaDSN', unicode_results='True')
    cursor = connection.cursor()

    files = [];
    day = ''
    try:
        cursor.execute('select year(CURRENT_DATE - 2), month(CURRENT_DATE - 2), day(CURRENT_DATE - 2 )')
        rows = cursor.fetchall()
        month = '{0:4d}{1:02d}'.format(rows[0].year, rows[0].month);
        day = '{0:4d}{1:02d}{2:02d}'.format(rows[0].year, rows[0].month, rows[0].day)
        
        BASEDIR = os.path.join(os.path.realpath(sys.path[0]), 'report')
        for setting in settings:
            folder = os.path.join(BASEDIR, setting['partnername'], month)
            filename = os.path.join(BASEDIR, setting['partnername'], month, setting['partnername'] + '_' + day) + '.xls'
        
    	    if not os.path.exists(folder):
                os.makedirs(folder)	
           
            wb = xlwt.Workbook()
        
            print str(datetime.datetime.now()) + '''  Pull data for "%s" ... ''' % setting['partnername'] 
            #print setting['sql']
            cursor.execute(setting['sql'])
            if AddSheet(wb, setting['name'], cursor, setting['row'], setting['col']):
                wb.save(filename)
                files.append(filename)
            else:
                print str(datetime.datetime.now()) + '''  No record for "%s" ''' % setting['partnername'] 

    except Exception as ex:
        print str(datetime.datetime.now()) + '''  Pull data for "%s" failed''' % setting['partnername']
        print Exception, ":", ex

    finally:
        connection.close()
     
    subject = day + ' report'

    send_mail(subject, 'This is a daily report by Tapjoy.cn\n\n', files)



if __name__ == "__main__":
    main()

