import pymysql
# connect the mysql in local server
conn = pymysql.connect(host = 'localhost',port = 3306,user= 'test',passwd='994821',db ='mytest')
cursor = conn.cursor() # get the cursor


def mysql_create_table (table_name,values_dict,key_dict,engine = innodb,foreign_key = None):
    """
    This funtion is to create a table in mysql 
    
    Parameter:
    _________
    
    table_name: string 
    
    values_dict: dict,whose keys and values are the value_name and type of the table 

    key_dict: list,and the fist items of the key is primary key ,
                and if the table has no primary key,the fist item should 
                be None 
    engine : defauly = innodb,the value shoud be in {myisam,HEAP,MEMORY,MERGE,MRG_MYISAM,INNODB,BDB,ECAMPLE,ARCHIVE,CSV};

    foreign_key:list ,default none 
    """
    values_len = len(values_len)
    key_len = len(key_dict)
    foreign_key_len = len(foreign_key)
    sql_statement = [
                     "create table '%s'( "]
sql_create_table = mysql_create_table('test_table',{id:int primary key})
print(sql_create_table)
cursor.execute(sql_create_table)

