


from database import Database as db_impl

__updated__ = "";


Database = db_impl;


    
if __name__ == "__main__":
    db = Database("mysql://openhab:openhab@localhost/openhab");
    db.get_items()
    print "Table for Living_Temp2 = {}".format(db.get_table_for_item("Living_Temp2"))
    print "connected"
        
