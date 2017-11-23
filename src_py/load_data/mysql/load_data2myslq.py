from load_data import load_data_xls 
import numpy 
import xlrd 
import pymysql
                
# get the table 
table = load_data_xls('./bank_data.xls',1)
# get the header of the table 
header = table.get_header()

# connect the mysql in local server
conn = pymysql.connect(host = 'localhost',port = 3306,user= 'test',passwd='994821',db ='mytest')
cursor = conn.cursor() # get the cursor


def create_table(table_name,value_dict = None,key = None,engine = 'innodb'):
    """This method is to create a table in mysql

    Parameters:
        table_name :string ,the name of the table 

        vuale_dit :dict,like {'value_name':type}

        key:list,the first item is primary key(is not None)

        engine : the store engine of the table,default innodb
    """
    if not  isinstance(table_name,str):
        raise ValueError("the  type of parameter table_name should"
                            "<string> ,but tpye of %s is passed"
                            % type(table_name))
    if not  isinstance(value_dict,dict):
        raise ValueError("the parameter table_name should be string,"
                        "but a %s was  passed"
                        % type(table_name))        
    sql = 'create  table ' + \
            table_name + ' '+'('
    print(sql)
    for key in value_dict:
        print(key,"the key !!!!!!")
        sql = sql + key + '  ' + value_dict[key] + ','
    # delete the last ',' in the sql statement
    sql = sql[0:len(sql)-1]
    sql = sql + ')' + 'engine = ' + engine
    return sql
sql_create_table = create_table('test_table',{"id":"int primary key"})       
print(sql_create_table,'------> the sql statement')
  #cursor.execute(sql_create_table)
cursor.execute(sql_create_table)
        
def add_data():
    

    pass 

def 

