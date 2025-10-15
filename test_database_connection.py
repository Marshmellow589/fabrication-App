import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

def test_database():
    print("🔍 Testing Database Connection and Models")
    print("=" * 50)
    
    try:
        from app.database import engine, SessionLocal
        from app.models import project
        
        print("1. Testing database connection...")
        with engine.connect() as conn:
            print("✅ Database connection successful")
        
        print("\n2. Testing Project model...")
        # Try to create a session and query
        db = SessionLocal()
        try:
            # Check if projects table exists
            result = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='projects'")
            tables = result.fetchall()
            if tables:
                print("✅ Projects table exists")
                # Try to count projects
                result = db.execute("SELECT COUNT(*) FROM projects")
                count = result.fetchone()[0]
                print(f"   Number of projects: {count}")
            else:
                print("❌ Projects table does not exist")
                
            # Check table structure
            result = db.execute("PRAGMA table_info(projects)")
            columns = result.fetchall()
            print(f"   Table columns: {[col[1] for col in columns]}")
            
        except Exception as e:
            print(f"❌ Database query error: {e}")
        finally:
            db.close()
            
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_database()
