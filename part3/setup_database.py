"""
Setup Database Script
This script generates the bcrypt hash for the admin password and updates seed.sql
"""
import sys
import os
import re

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from hbnb.app.extensions import bcrypt
from hbnb.app import create_app

def generate_admin_hash():
    """Generate bcrypt hash for admin password"""
    print("=" * 60)
    print("Generating Admin Password Hash")
    print("=" * 60)
    
    # Create Flask app context for bcrypt
    app = create_app()
    
    with app.app_context():
        password = "admin1234"
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        print(f"\nPassword: {password}")
        print(f"Hashed: {hashed_password}")
        
        return hashed_password

def update_seed_file(hashed_password):
    """Update seed.sql with the generated hash"""
    print("\n" + "=" * 60)
    print("Updating seed.sql with password hash")
    print("=" * 60)
    
    # Read seed.sql
    with open('seed.sql', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace placeholder with actual hash
    updated_content = re.sub(
        r'\$2b\$12\$HASH_WILL_BE_HERE',
        hashed_password,
        content
    )
    
    # Write to seed_updated.sql
    with open('seed_updated.sql', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("\n✅ seed_updated.sql created successfully!")
    print("\nFiles ready:")
    print("  - schema.sql (table definitions)")
    print("  - seed_updated.sql (initial data with hashed password)")

def display_info():
    """Display information about the initial data"""
    print("\n" + "=" * 60)
    print("Initial Data Information")
    print("=" * 60)
    print("\n📧 Admin User:")
    print("  ID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1")
    print("  Email: admin@hbnb.io")
    print("  Password: admin1234")
    print("  Is Admin: True")
    print("\n🏠 Amenities:")
    print("  1. WiFi (ID: a1b2c3d4-e5f6-4a5b-9c8d-1e2f3a4b5c6d)")
    print("  2. Swimming Pool (ID: b2c3d4e5-f6a7-5b6c-ad9e-2f3a4b5c6d7e)")
    print("  3. Air Conditioning (ID: c3d4e5f6-a7b8-6c7d-be0f-3a4b5c6d7e8f)")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        # Generate hash
        hashed_password = generate_admin_hash()
        
        # Update seed file
        update_seed_file(hashed_password)
        
        # Display info
        display_info()
        
        print("\n🎉 Setup complete! Run 'python run_sql_scripts.py' to create the database.")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
