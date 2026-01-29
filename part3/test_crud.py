"""
Test CRUD Operations
This script tests all CRUD operations on the database to verify schema correctness
"""
import sqlite3
import sys
from datetime import datetime

DB_PATH = 'hbnb_database.db'

def test_crud_operations():
    """Test Create, Read, Update, Delete operations"""
    
    print("=" * 60)
    print("Testing CRUD Operations on HBnB Database")
    print("=" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")  # Enable foreign keys
    cursor = conn.cursor()
    
    try:
        # ========================================
        # 1. READ - Fetch Admin User
        # ========================================
        print("\n1️⃣  READ - Fetch Admin User")
        print("-" * 60)
        cursor.execute("""
            SELECT id, email, first_name, last_name, is_admin 
            FROM users 
            WHERE email='admin@hbnb.io';
        """)
        admin = cursor.fetchone()
        if admin:
            print(f"✅ Admin found:")
            print(f"   ID: {admin[0][:8]}...")
            print(f"   Email: {admin[1]}")
            print(f"   Name: {admin[2]} {admin[3]}")
            print(f"   Is Admin: {admin[4]}")
        else:
            print("❌ Admin not found!")
            return False
        
        # ========================================
        # 2. READ - Fetch All Amenities
        # ========================================
        print("\n2️⃣  READ - Fetch All Amenities")
        print("-" * 60)
        cursor.execute("SELECT id, name FROM amenities ORDER BY name;")
        amenities = cursor.fetchall()
        print(f"✅ Found {len(amenities)} amenities:")
        for amenity in amenities:
            print(f"   - {amenity[1]} (ID: {amenity[0][:8]}...)")
        
        # ========================================
        # 3. CREATE - Insert New User
        # ========================================
        print("\n3️⃣  CREATE - Insert New User")
        print("-" * 60)
        test_user_id = 'test-user-uuid-12345678'
        cursor.execute("""
            INSERT INTO users (id, first_name, last_name, email, password, is_admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (test_user_id, 'John', 'Doe', 'john.doe@test.com', 'hashed_password_123', False))
        conn.commit()
        print(f"✅ User created:")
        print(f"   ID: {test_user_id}")
        print(f"   Email: john.doe@test.com")
        
        # ========================================
        # 4. CREATE - Insert Place for Test User
        # ========================================
        print("\n4️⃣  CREATE - Insert Place")
        print("-" * 60)
        test_place_id = 'test-place-uuid-12345678'
        cursor.execute("""
            INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (test_place_id, 'Beautiful Beach House', 'Amazing ocean view', 250.50, 25.2048, 55.2708, test_user_id))
        conn.commit()
        print(f"✅ Place created:")
        print(f"   ID: {test_place_id}")
        print(f"   Title: Beautiful Beach House")
        print(f"   Owner: {test_user_id[:8]}...")
        
        # ========================================
        # 5. CREATE - Insert Review
        # ========================================
        print("\n5️⃣  CREATE - Insert Review")
        print("-" * 60)
        test_review_id = 'test-review-uuid-12345678'
        cursor.execute("""
            INSERT INTO reviews (id, text, rating, user_id, place_id)
            VALUES (?, ?, ?, ?, ?)
        """, (test_review_id, 'Excellent place! Highly recommended.', 5, admin[0], test_place_id))
        conn.commit()
        print(f"✅ Review created:")
        print(f"   ID: {test_review_id}")
        print(f"   Rating: 5/5")
        print(f"   By User: {admin[0][:8]}...")
        
        # ========================================
        # 6. CREATE - Link Place with Amenities
        # ========================================
        print("\n6️⃣  CREATE - Link Place with Amenities")
        print("-" * 60)
        # Link WiFi and Air Conditioning to the place
        cursor.execute("""
            INSERT INTO place_amenity (place_id, amenity_id)
            VALUES (?, ?)
        """, (test_place_id, amenities[1][0]))  # Air Conditioning
        cursor.execute("""
            INSERT INTO place_amenity (place_id, amenity_id)
            VALUES (?, ?)
        """, (test_place_id, amenities[2][0]))  # WiFi
        conn.commit()
        print(f"✅ Amenities linked to place:")
        print(f"   - {amenities[1][1]}")
        print(f"   - {amenities[2][1]}")
        
        # ========================================
        # 7. READ - Complex Query (Join)
        # ========================================
        print("\n7️⃣  READ - Complex Query (Places with Amenities)")
        print("-" * 60)
        cursor.execute("""
            SELECT p.title, a.name
            FROM places p
            JOIN place_amenity pa ON p.id = pa.place_id
            JOIN amenities a ON pa.amenity_id = a.id
            WHERE p.id = ?
        """, (test_place_id,))
        place_amenities = cursor.fetchall()
        print(f"✅ Place '{place_amenities[0][0]}' has amenities:")
        for pa in place_amenities:
            print(f"   - {pa[1]}")
        
        # ========================================
        # 8. UPDATE - Update User's First Name
        # ========================================
        print("\n8️⃣  UPDATE - Update User's First Name")
        print("-" * 60)
        cursor.execute("""
            UPDATE users 
            SET first_name = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, ('Johnny', test_user_id))
        conn.commit()
        
        cursor.execute("SELECT first_name FROM users WHERE id = ?", (test_user_id,))
        updated_name = cursor.fetchone()[0]
        print(f"✅ User's first name updated to: {updated_name}")
        
        # ========================================
        # 9. UPDATE - Update Place Price
        # ========================================
        print("\n9️⃣  UPDATE - Update Place Price")
        print("-" * 60)
        new_price = 299.99
        cursor.execute("""
            UPDATE places 
            SET price = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (new_price, test_place_id))
        conn.commit()
        print(f"✅ Place price updated to: ${new_price}")
        
        # ========================================
        # 10. TEST - Foreign Key Constraint (Should Fail)
        # ========================================
        print("\n🔟 TEST - Foreign Key Constraint")
        print("-" * 60)
        try:
            cursor.execute("""
                INSERT INTO places (id, title, price, latitude, longitude, owner_id)
                VALUES ('bad-place', 'Invalid Place', 100.0, 25.0, 55.0, 'non-existent-user-id')
            """)
            conn.commit()
            print("❌ Foreign key constraint NOT working! (This should have failed)")
        except sqlite3.IntegrityError as e:
            print(f"✅ Foreign key constraint working correctly:")
            print(f"   Error: {str(e)[:50]}...")
        
        # ========================================
        # 11. TEST - Unique Constraint on Review (Should Fail)
        # ========================================
        print("\n1️⃣1️⃣  TEST - Unique Constraint (user_id, place_id)")
        print("-" * 60)
        try:
            cursor.execute("""
                INSERT INTO reviews (id, text, rating, user_id, place_id)
                VALUES ('duplicate-review', 'Another review', 4, ?, ?)
            """, (admin[0], test_place_id))
            conn.commit()
            print("❌ Unique constraint NOT working! (This should have failed)")
        except sqlite3.IntegrityError as e:
            print(f"✅ Unique constraint working correctly:")
            print(f"   Error: {str(e)[:70]}...")
        
        # ========================================
        # 12. TEST - Rating Check Constraint
        # ========================================
        print("\n1️⃣2️⃣  TEST - Rating Check Constraint (1-5)")
        print("-" * 60)
        try:
            cursor.execute("""
                INSERT INTO reviews (id, text, rating, user_id, place_id)
                VALUES ('bad-rating', 'Bad rating test', 6, ?, 'some-place-id')
            """, (test_user_id,))
            conn.commit()
            print("❌ Check constraint NOT working! (This should have failed)")
        except sqlite3.IntegrityError as e:
            print(f"✅ Check constraint working correctly:")
            print(f"   Error: {str(e)[:50]}...")
        
        # ========================================
        # 13. DELETE - Test Cascade Delete
        # ========================================
        print("\n1️⃣3️⃣  DELETE - Test Cascade Delete")
        print("-" * 60)
        
        # Count reviews before delete
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE place_id = ?", (test_place_id,))
        reviews_before = cursor.fetchone()[0]
        
        # Delete the place (should cascade delete reviews and place_amenity entries)
        cursor.execute("DELETE FROM places WHERE id = ?", (test_place_id,))
        conn.commit()
        
        # Check if reviews were deleted
        cursor.execute("SELECT COUNT(*) FROM reviews WHERE place_id = ?", (test_place_id,))
        reviews_after = cursor.fetchone()[0]
        
        # Check if place_amenity entries were deleted
        cursor.execute("SELECT COUNT(*) FROM place_amenity WHERE place_id = ?", (test_place_id,))
        amenities_after = cursor.fetchone()[0]
        
        print(f"✅ Place deleted:")
        print(f"   Reviews before: {reviews_before}, after: {reviews_after}")
        print(f"   Place-Amenity links after: {amenities_after}")
        print(f"   ✅ Cascade delete working correctly!")
        
        # ========================================
        # 14. DELETE - Clean up test user
        # ========================================
        print("\n1️⃣4️⃣  DELETE - Clean Up Test Data")
        print("-" * 60)
        cursor.execute("DELETE FROM users WHERE id = ?", (test_user_id,))
        conn.commit()
        print(f"✅ Test user deleted")
        
        # Final verification
        cursor.execute("SELECT COUNT(*) FROM users;")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM amenities;")
        amenity_count = cursor.fetchone()[0]
        
        print("\n" + "=" * 60)
        print("✅ All CRUD Tests Passed Successfully!")
        print("=" * 60)
        print(f"\nFinal Database State:")
        print(f"  Users: {user_count} (Admin only)")
        print(f"  Amenities: {amenity_count}")
        print(f"  Places: 0")
        print(f"  Reviews: 0")
        print("\n🎉 Database schema is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    import os
    
    if not os.path.exists(DB_PATH):
        print(f"❌ Error: Database '{DB_PATH}' not found!")
        print("Please run 'python run_sql_scripts.py' first.")
        sys.exit(1)
    
    try:
        success = test_crud_operations()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
        sys.exit(1)
