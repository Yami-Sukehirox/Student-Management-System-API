from database import engine

try:
    with engine.connect() as connection:
        print("Successfully connected to mySQL!")
except Exception as e:
    print("Database connection failed")        
    print (e)