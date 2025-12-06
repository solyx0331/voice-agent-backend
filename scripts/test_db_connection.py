"""
Database Connection Test Script
Tests the database connection and provides diagnostics
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.config import settings
from app.core.database import engine, prepare_database_url
from sqlalchemy import text
import socket


def test_dns_resolution(hostname: str) -> bool:
    """Test if hostname can be resolved"""
    try:
        port = 5432
        if ":" in hostname:
            hostname, port = hostname.split(":")
            port = int(port)
        
        print(f"Testing DNS resolution for: {hostname}")
        ip_address = socket.gethostbyname(hostname)
        print(f"✓ DNS resolution successful: {hostname} -> {ip_address}")
        return True
    except socket.gaierror as e:
        print(f"✗ DNS resolution failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during DNS test: {e}")
        return False


def test_port_connectivity(hostname: str, port: int = 5432) -> bool:
    """Test if port is reachable"""
    try:
        print(f"Testing port connectivity: {hostname}:{port}")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((hostname, port))
        sock.close()
        
        if result == 0:
            print(f"✓ Port {port} is reachable")
            return True
        else:
            print(f"✗ Port {port} is not reachable (connection refused)")
            return False
    except Exception as e:
        print(f"✗ Error testing port: {e}")
        return False


async def test_database_connection():
    """Test actual database connection"""
    print("\n" + "="*60)
    print("Database Connection Test")
    print("="*60)
    
    # Show configuration
    print(f"\nDatabase URL (masked):")
    db_url = settings.DATABASE_URL
    if "@" in db_url:
        parts = db_url.split("@")
        masked_url = f"{parts[0].split(':')[0]}://***:***@{parts[1]}"
        print(f"  {masked_url}")
    else:
        print(f"  {db_url}")
    
    # Extract hostname
    if "@" in db_url:
        host_part = db_url.split("@")[1]
        if ":" in host_part:
            hostname = host_part.split(":")[0]
            port = int(host_part.split(":")[1].split("/")[0])
        else:
            hostname = host_part.split("/")[0]
            port = 5432
    else:
        print("✗ Could not parse database URL")
        return False
    
    print(f"\nHostname: {hostname}")
    print(f"Port: {port}")
    
    # Test DNS resolution
    print("\n1. Testing DNS Resolution...")
    dns_ok = test_dns_resolution(hostname)
    
    if not dns_ok:
        print("\n✗ DNS resolution failed. Cannot proceed with connection test.")
        print("\nTroubleshooting steps:")
        print("  1. Check your internet connection")
        print("  2. Verify the hostname in your Supabase dashboard")
        print("  3. Check if your Supabase project is active (not paused)")
        print("  4. Try pinging the hostname: ping db.grxzzijboqadlibsaxqa.supabase.co")
        return False
    
    # Test port connectivity
    print("\n2. Testing Port Connectivity...")
    port_ok = test_port_connectivity(hostname, port)
    
    if not port_ok:
        print("\n✗ Port is not reachable. Firewall or network might be blocking.")
        return False
    
    # Test database connection
    print("\n3. Testing Database Connection...")
    try:
        prepared_url = prepare_database_url(settings.DATABASE_URL)
        print(f"  Using prepared URL: {prepared_url.split('@')[0]}@***")
        
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✓ Database connection successful!")
            print(f"  PostgreSQL version: {version.split(',')[0]}")
            return True
    except Exception as e:
        error_str = str(e)
        print(f"✗ Database connection failed: {error_str[:200]}")
        
        if "authentication failed" in error_str.lower():
            print("\n  → Authentication failed. Check your database password.")
        elif "database" in error_str.lower() and "does not exist" in error_str.lower():
            print("\n  → Database does not exist. Check your database name.")
        else:
            print("\n  → Check your database credentials and connection string.")
        
        return False


async def main():
    """Main function"""
    try:
        success = await test_database_connection()
        
        print("\n" + "="*60)
        if success:
            print("✓ All tests passed! Database connection is working.")
        else:
            print("✗ Connection test failed. See details above.")
        print("="*60)
        
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

