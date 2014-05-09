#####Functions to work the state dept cables collection
#######


import re
from datetime import datetime

from declass.utils.database import DBCONNECT



def cable_datetime_main(db, cable_table='statedeptcables', cable_dt_table='CableDatetime',
        fields=['DOC_NBR', 'MSGTEXT'], skip_empty_text=True, limit=None):
    """
    Wraps up the function below, extracts cables and updates CableDatetime 
    table. Mostly a use case of utils here. 
    """

    cables = get_cables(db, cable_table, fields, skip_empty_text, limit)

    for cable in cables:
        doc_num = cable['DOC_NBR']
        text = cable['MSGTEXT']
        dts = set(dt_find(text))
        dts = [dt_clean(dt) for dt in dts]
        good_dt = None
        for dt in dts:
            try:
                good_dt = datetime_parse(dt)
            except ValueError:
                pass
        _update_table(db, doc_num, good_dt, cable_dt_table)


def get_cables(db, table_name='statedeptcables', 
        fields=['DOC_NBR', 'MSGTEXT'], skip_empty_text=True, 
        limit=None, offset=None):
    """
    Retrieves cables from declass DB.
    """
    sql = 'select %s from %s'%(','.join(fields), table_name)
    if skip_empty_text:
        sql = (table_name + " where MSGTEXT!=''").join(sql.split(table_name))
    if limit:
        sql = sql + ' limit %s'%limit
    if offset:
        sql = sql + ' offset %s'%offset
    return db.run_query(sql)


def dt_find(text):
    """
    Finds datetime strings in text.
    
    Parameters
    ----------
    text : string
    """
    regex = re.compile(
            r'\d{6,7} {,1}[A-Z]{,2} {,1}[A-Z]{2,10} {,1}\d{2}')
    return regex.findall(text)
   

def datetime_parse(dt):
    """
    Parses datetime strings from the various cables formats.
    
    Parameters
    ----------
    dt : string

    Returns:
    -------
    dt : string
       in '%Y-%m-%d %H:%M' format
    """
    try:
        dt = datetime.strptime(dt, '%d%H%M %b %y')
    except ValueError:
        dt = datetime.strptime(dt, '%d%H%M %B %y')

    return dt.strftime('%Y-%m-%d %H:%M')


def dt_clean(dt):
    """
    Takes a datetime string returned by dt_find() and cleans it. 
    """
    dt = dt.replace('Z', '')
    dt = dt.replace('OF', '')
    return dt


def _update_table(db, doc_num, dt, table_name='CableDatetime'):
    sql = "insert ignore into %s Values('%s', '%s');"%(
            table_name, doc_num, dt)
    db.run_query(sql)


def get_body(cable):
    """
    Retrives the cable text body. 

    Parameters
    ----------
    cables : str
        cable text

    Returns
    -------
    list of strings
        cable body paragraphs
    """
    cable = re.sub(r'(\n{,2}[A-Z]+|)\n+PAGE.*\n+', ' ', cable)
    cable = re.sub(r'\n([ A-Z\(\)"])', ' \g<1>', cable)
    return re.findall(r'\d\..*', cable)
    

