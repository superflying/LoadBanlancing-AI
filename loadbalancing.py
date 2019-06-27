import pyodbc
import csv
cnxn = pyodbc.connect('DSN=jsculte_new;UID=dcbo;PWD=dcbo')
cursor = cnxn.cursor()
#连接数据库，并创建游标
sql = '''
SELECT COUNT(a.OSS_ID) , 
a.DATE_ID AS 'DATE',
a.HOUR_ID AS 'HOUR',
a.EUtranCellFDD AS 'CELL',

SUM(pmPdcpVolDlDrb) AS 'PdcpVolDlDrb',
round(SUM(pmPdcpVolDlDrb-pmPdcpVolDlDrbLastTTI)/(SUM(pmUeThpTimeDl/1000)+0.01),2) AS 'Average_UE_DL_Throughput',
round(SUM(pmRrcConnLevSum)/(SUM(pmRrcConnLevSamp)+0.01),2) AS 'RRC_Connected',
round(SUM(pmErabLevSum)/(SUM(pmErabLevSamp)+0.01),2) AS 'ERAB_Connected',
round(SUM(pmPrbUsedUlDtch+pmPrbUsedUlSrb)/(60*60*1000),0) AS 'UL_PRB_USEAGE',
round((SUM(pmPrbUsedDlDtch+pmPrbUsedDlBcch+pmPrbUsedDlPcch)+SUM(pmPrbUsedDlSrbFirstTrans)*(1+SUM(pmPrbUsedDlReTrans)/SUM(pmPrbUsedDlFirstTrans)))/(60*60*1000),0) AS'DL_PRB_USEAGE',
COUNT(a.OSS_ID) 
FROM dc.DC_E_ERBS_EUTRANCELLFDD_RAW a WHERE 
a.PERIOD_DURATION=15 AND
a.MONTH_ID=6 AND 
a.DAY_ID IN (20) AND
a.HOUR_ID IN (10) AND
a.EUtranCellFDD LIKE 'YZEAFL345245_01%'
GROUP BY a.DATE_ID,
a.HOUR_ID,
a.EUtranCellFDD
'''
#sql语句
cursor.execute(sql)

rows = cursor.fetchall()
title = ['Count','Date','Hour','Cell','PdcpVolDlDrb','UE下行平均速率','RRC_Connected','ERAB_Connected','UL_PRB_USEAGE','DL_PRB_USEAGE','Count']
#写入标题，指标命名
csv_file = open('LB_kpi.csv','w',newline='',encoding='utf-8-sig')
#新建csv文件存放指标
writer = csv.writer(csv_file)
writer.writerow(title)
for row in rows:
	writer.writerow(row)
	#写入取出的具体指标
csv_file.close
#保存文件