from models import create_tables

# Function for creating tables in database when run Docker
if __name__ == '__main__':
    create_tables()
    print("Database tables created")
