import pandas as pd
#to import 'text' for robust SQL query handling
from sqlalchemy import create_engine, text
from typing import Optional


DB_URL = "mysql+pymysql://root:srihari@localhost:3306/dd_stockanalysis" 

def connect_db():
    
    """Create SQLAlchemy engine."""
    try:
        engine = create_engine(DB_URL)
        return engine
    except Exception as e:
        print(f"❌ Error connecting to database. Check credentials or server status: {e}")
        # Re-raise the exception so calling functions know the connection failed
        raise 

def save_to_db(df: pd.DataFrame, table_name: str, if_exists: str = 'replace'):
    """
    Saves a DataFrame to a specified database table and explicitly commits the changes.
    FIXED: Uses engine.begin() to ensure the transaction is committed.
    """
    engine = connect_db()
    
    try:
        #  Open a connection and start a transaction block. 
        # The 'with engine.begin() as conn:' block automatically manages commit/rollback.
        with engine.begin() as conn: 
            
            print(f"Loading data into table: {table_name}...")
            
            #Perform the SQL insertion within the transaction
            df.to_sql(
                table_name, 
                con=conn, #the connection object from the transaction
                if_exists=if_exists, 
                index=False, 
                chunksize=1000
            )
        
        # This point is reached only if the commit was successful
        print(f"✅ Successfully saved {len(df)} records to {table_name}.")
        
    except Exception as e:
        print(f"❌ Error saving data to database: {e}")

def read_from_db(query: str) -> Optional[pd.DataFrame]:
    """Reads data from the database using a custom SQL query and returns a DataFrame."""
    try:
        engine = connect_db()
        # Log the start of the query for debugging
        print(f"Executing query: {query.strip().splitlines()[0][:60]}...")
        
        # Using text() ensures compatibility with modern SQLAlchemy
        df = pd.read_sql(text(query), con=engine)
        
        print(f"✅ Successfully read {len(df)} records.")
        return df
    except Exception as e:
    
        print(f"❌ Error reading data from database: {e}")
        return None


if __name__ == "__main__":
    """This block runs ONLY when you execute 'python db.py' directly."""
    print("\nRunning Database Connection Test")
    
    try:
        # Attempt to create the engine
        engine = connect_db()
        print("✅ SQLAlchemy Engine created successfully.")
        
        # Attempt to open and close a direct connection
        with engine.connect() as connection:
            print("✅ Database connection established and closed successfully!")
            
            # Test reading data from a required table (e.g., stocks_metrics)
            test_query = "SELECT ticker, yearly_return FROM stocks_metrics LIMIT 1"
            df_test = pd.read_sql(text(test_query), con=connection)
            
            if not df_test.empty:
                print(f"✅ Data read test successful! Table 'stocks_metrics' is accessible.")
            else:
                print("⚠️ Table 'stocks_metrics' is accessible but empty (expected at this stage).")
                
    except Exception as e:
        print("\n❌ FINAL TEST FAILED. Fix the DB_URL or check your MySQL server.")
    finally:
        print("Test Complete")