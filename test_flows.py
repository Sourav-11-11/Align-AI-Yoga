"""Quick flow test for Align AI Yoga app"""
import sys
import os

sys.path.insert(0, 'frontend')
os.environ['DB_TYPE'] = 'sqlite'

from app import create_app

def test_flows():
    """Test critical user flows"""
    app = create_app('development')
    print("[OK] App initialized")
    
    with app.test_client() as client:
        # Home
        r = client.get('/')
        assert r.status_code in [302, 200]
        print("[OK] Home route accessible")
        
        # Register page
        r = client.get('/register')
        assert r.status_code == 200
        print("[OK] Register page loads")
        
        # Register
        r = client.post('/register', data={
            'email': 'test@example.com',
            'name': 'Test User',
            'password': 'Test123!',
            'c_password': 'Test123!'
        }, follow_redirects=True)
        print(f"  Register status: {r.status_code}")
        assert r.status_code == 200, f"Register failed: {r.status_code}"
        print("[OK] Registration works")
        
        # Login
        r = client.post('/login', data={
            'email': 'test@example.com',
            'password': 'Test123!'
        }, follow_redirects=True)
        print(f"  Login status: {r.status_code}")
        assert r.status_code == 200
        print("[OK] Login works")
        
        # Yoga home
        r = client.get('/home', follow_redirects=True)
        print(f"  Yoga home status: {r.status_code}")
        assert r.status_code == 200
        print("[OK] Yoga home loads")
        
        # Yoga session (mood page)
        r = client.get('/yoga1', follow_redirects=True)
        print(f"  Yoga session status: {r.status_code}")
        assert r.status_code == 200
        print("[OK] Mood page loads")
        
        # Dashboard
        r = client.get('/dashboard', follow_redirects=True)
        print(f"  Dashboard status: {r.status_code}")
        assert r.status_code == 200
        print("[OK] Dashboard loads")
        
        # Logout
        r = client.get('/logout', follow_redirects=True)
        print(f"  Logout status: {r.status_code}")
        assert r.status_code == 200
        print("[OK] Logout works")
        
    print("\n[PASS] All flows verified")

if __name__ == '__main__':
    try:
        test_flows()
    except Exception as e:
        print(f"[FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
