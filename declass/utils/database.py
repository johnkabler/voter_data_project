"""
Collection of functions for connecting to the database.
"""
import pymysql


class DBCONNECT(object):
    """
    Connects to a MySQL DB and executes basic queiries.

    Example
    -------
    dbCon = DBCONNECT(host_name, db_name, user_name, pwd)
    table_name = 'declassification'
    doc_id = 242518
    fields = 'body, title'
    doc = dbCon.get_row_by_id(row_id=doc_id, table_name=table_name,
            fields=fields)
    doc_list = dbCon.get_rows_by_idlist(id_list=[242518, 317509],
            table_name=table_name, fields=fields)

    Notes
    -----
    TODO : figure out why pymysql cursor does not execute 'where in list' type statements

    """
    def __init__(self, host_name, db_name, user_name, pwd):
        """
        Initializes the class and pymysql cursor object.

        Parameters
        ----------
        host_name : string
        db_name : string
        user_name : string
        pwd : string
        """
        self.conn = pymysql.connect(host=host_name, user=user_name, passwd=pwd, db=db_name)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        self.conn.autocommit(1)

    def get_row_by_id(self, row_id, table_name, fields='*'):
        """
        Parameters
        ----------
        row_id : string or int
        table_name : string
        fields : string
            format = 'field1, field2, ...'; default is all fields

        Returns
        -------
        output : dict

        Notes
        -----
        assumes table has an 'id' entry
        """
        sql = 'select %s from Document where id = %s'%(fields, row_id)
        self.cursor.execute(sql)
        output = self.cursor.fetchall()
        return output[0]

    def get_rows_by_idlist(self, id_list, table_name, fields='*', get_iter=False):
        """
        Parameters
        ----------
        id_list : list of strings or ints
        table_name : string
        fields : string
            format = 'field1, field2, ...'; default is all fields

        Returns
        -------
        output_list : list

        Notes
        -----
        assumes table has an 'id' entry
        TODO: remove after sort out pymysql 'where in ' bug

        """
        row_iter = self.__get_rows_by_idlist_iter(id_list, table_name, fields)
        if get_iter:
            return row_iter
        else:
            row = [row for row in row_iter]
            return row

    def run_query(self, sql):
        try:
            self.cursor.execute(sql)
            output = self.cursor.fetchall()
            return output
        except pymysql.err.InternalError, e:
            print 'A MySQL error occured!\n'
            print 'If you need to consult the DB schema please use either '\
            'the DBCONNECT.get_field_info() or DBCONNECT'\
            '.get_table_names() methods.\n'
            print 'Error details:'
            return e

    def __get_rows_by_idlist_iter(self, id_list, table_name, fields='*'):
        """
        Parameters
        ----------
        id_list : list of strings or ints
        table_name : string
        fields : string
            format = 'field1, field2, ...'; default is all fields

        Returns
        -------
        output_list : list

        Notes
        -----
        assumes table has an 'id' entry
        TODO: remove after sort out pymysql 'where in ' bug

        """

        return (self.get_row_by_id(row_id=row_id, table_name=table_name,
            fields=fields) for row_id in id_list)


    def get_table_names(self):
        """
        Fetches all table names in the DB.

        Returns
        -------
        output : list of strings
        """
        sql = 'show tables'
        self.cursor.execute(sql)
        temp_output = self.cursor.fetchall()
        output = [entry['Tables_in_declassification'] for entry in temp_output]
        return output

    def get_field_info(self, table_name):
        """
        Fetches all field names and type for a given table

        Returns
        -------
        output : list of tuples (field_name, column_type)
        """
        sql = 'show columns from %s'%table_name
        self.cursor.execute(sql)
        temp_output = self.cursor.fetchall()
        #output = [entry[:2] for entry in temp_output]
        return temp_output

    def close(self):
        """
        Closes the mysql connection.

        Notes
        -----
        Not strictly necessary, but good practice to close session after use.
        """
        self.conn.close()



if __name__ == '__main__':

    dbCon = DBCONNECT(host_name, db_name, user_name, pwd)
    print dbCon.get_table_names()
    #table_name = 'declassification'
    table_name = 'DocumentPair'
    print dbCon.get_field_info(table_name)
    #doc_id = 242518
    #fields = 'body'
    #doc = dbCon.get_row_by_id(row_id=doc_id, table_name=table_name, fields=fields)
    #print doc
    #doc_list = dbCon.get_rows_by_idlist(id_list=[242518, 317509], table_name=table_name, fields=fields)
    #print 'doc list ', doc_list
    #doc_list_iter = dbCon.get_rows_by_idlist(id_list=[242518, 317509], table_name=table_name, fields=fields, get_iter=True)
    #print 'doc1 ', doc_list_iter.next()
    #print 'doc2', doc_list_iter.next()

    #query = dbCon.run_query('select id, title from Document where sdfsd;')
    #print query
    #table_names = dbCon.get_table_names()
    #print table_names
    #field_info = dbCon.get_field_info(table_name='Document')
    #print column_info
    dbCon.close()


