from PyQt6.QtSql import QSqlDatabase, QSqlQuery

def initialize_database(db_name):
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_name)

    if not db.open():
        return False
    
    query = QSqlQuery()
    # SQL to make a table if it doesn't exist
    query.exec(""" 
               CREATE TABLE IF NOT EXISTS costs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT, 
                    category TEXT,
                    amount REAL,
                    description TEXT
               ) 
               """)
    return True

def get_cost():
    query = QSqlQuery("SELECT * FROM costs ORDER BY date DESC")
    costs = []
    while query.next():
        # Populate 1 cost for each column of database
        cost = [query.value(i) for i in range(5)]
        costs.append(cost)
    return costs

def add_cost(date, category, amount, description):
    query = QSqlQuery()
    query.prepare("""
                  INSERT INTO costs (date, category, amount, description)
                  VALUES (?, ?, ?, ?)
                  """)
    query.addBindValue(date)
    query.addBindValue(category)
    query.addBindValue(amount)
    query.addBindValue(description)

    return query.exec()

def delete_cost(id):
    query = QSqlQuery()
    query.prepare("DELETE FROM costs WHERE id = ?")
    query.addBindValue(id)

    return query.exec()