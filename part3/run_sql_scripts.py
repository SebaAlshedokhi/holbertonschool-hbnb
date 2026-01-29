"""
Run SQL Scripts
This script executes schema.sql and seed_updated.sql to create and populate the database
"""
import sqlite3
import os
import sys

DB_PATH = 'hbnb_database.db'

def execute_sql_file(db_path, sql_file):
    """Execute a SQL file against the database"""
    print(f"\n📄 Executing {sql_file}...")
    
    if not os.path.exists(sql_file):
        print(f"❌ Error: {sql_file} not found!")
        return False
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Enable foreign keys
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Execute the script
        cursor.executescript(sql_script)
        conn.commit()
        
        print(f"✅ {sql_file} executed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error executing {sql_file}: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

def verify_database(db_path):
    """Verify the database was created correctly"""
    print("\n" + "=" * 60)
    print("Verifying Database")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        tables = cursor.fetchall()
        print(f"\n📊 Tables created ({len(tables)}):")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
            count = cursor.fetchone()[0]
            print(f"  ✅ {table[0]} ({count} rows)")
        
        # Check admin user
        print("\n👤 Admin User:")
        cursor.execute("""
            SELECT id, email, first_name, last_name, is_admin 
            FROM users 
            WHERE id='36c9050e-ddd3-4c3b-9731-9f487208bbc1';
        """)
        admin = cursor.fetchone()
        if admin:
            print(f"  ✅ ID: {admin[0]}")
            print(f"  ✅ Email: {admin[1]}")
            print(f"  ✅ Name: {admin[2]} {admin[3]}")
            print(f"  ✅ Is Admin: {admin[4]}")
        else:
            print("  ❌ Admin user not found!")
        
        # Check amenities
        print("\n🏠 Amenities:")
        cursor.execute("SELECT id, name FROM amenities ORDER BY name;")
        amenities = cursor.fetchall()
        for amenity in amenities:
            print(f"  ✅ {amenity[1]} (ID: {amenity[0][:8]}...)")
        
        # Check indexes
        print("\n📑 Indexes:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name LIKE 'idx_%';")
        indexes = cursor.fetchall()
        for idx in indexes:
            print(f"  ✅ {idx[0]}")
        
    except Exception as e:
        print(f"\n❌ Error verifying database: {e}")
        
    finally:
        conn.close()

def main():
    """Main execution function"""
    print("=" * 60)
    print("HBnB Database Setup")
    print("=" * 60)
    
    # Check if seed_updated.sql exists
    if not os.path.exists('seed_updated.sql'):
        print("\n❌ Error: seed_updated.sql not found!")
        print("Please run 'python setup_database.py' first.")
        sys.exit(1)
    
    # Remove old database if exists
    if os.path.exists(DB_PATH):
        print(f"\n🗑️  Removing old database: {DB_PATH}")
        os.remove(DB_PATH)
    
    # Execute schema
    if not execute_sql_file(DB_PATH, 'schema.sql'):
        print("\n❌ Failed to create schema. Aborting.")
        sys.exit(1)
    
    # Execute seed data
    if not execute_sql_file(DB_PATH, 'seed_updated.sql'):
        print("\n❌ Failed to insert seed data. Aborting.")
        sys.exit(1)
    
    # Verify database
    verify_database(DB_PATH)
    
    print("\n" + "=" * 60)
    print("✅ Database setup complete!")
    print("=" * 60)
    print(f"\nDatabase: {DB_PATH}")
    print("Run 'python test_crud.py' to test CRUD operations.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
