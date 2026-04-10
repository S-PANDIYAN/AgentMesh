"""
Backend System Testing Suite
Comprehensive tests for database, authentication, file management, and API endpoints
"""
import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta

# Database tests
class TestDatabaseConfiguration:
    """Test database initialization and connection"""
    
    def test_database_initialization(self):
        """Test database initialization"""
        from backend.database import db_manager
        
        db_manager.initialize()
        assert db_manager.is_connected()
    
    def test_session_creation(self):
        """Test session creation"""
        from backend.database import db_manager
        
        session = db_manager.get_session()
        assert session is not None
        session.close()
    
    def test_table_creation(self):
        """Test table creation"""
        from backend.database import db_manager
        from backend.db_models import User, APIKey, Analysis
        
        db_manager.create_tables()
        
        session = db_manager.get_session()
        try:
            # Check if tables exist
            inspector = db_manager.get_inspector()
            tables = inspector.get_table_names()
            
            assert 'users' in tables
            assert 'api_keys' in tables
            assert 'analyses' in tables
        finally:
            session.close()


# Authentication tests
class TestAuthentication:
    """Test authentication system"""
    
    def test_user_registration(self):
        """Test user registration"""
        from backend.auth import UserManager
        from backend.database import db_manager
        
        session = db_manager.get_session()
        try:
            user, api_key = UserManager.create_user(
                session=session,
                email="test@example.com",
                username="testuser",
                password="password123"
            )
            
            assert user is not None
            assert user.email == "test@example.com"
            assert api_key is not None
        finally:
            session.close()
    
    def test_user_authentication(self):
        """Test user authentication"""
        from backend.auth import UserManager
        from backend.database import db_manager
        
        session = db_manager.get_session()
        try:
            # Create user
            user, _ = UserManager.create_user(
                session=session,
                email="auth@example.com",
                username="authuser",
                password="password123"
            )
            
            # Authenticate
            authenticated = UserManager.authenticate_user(
                session=session,
                email="auth@example.com",
                password="password123"
            )
            
            assert authenticated is not None
            assert authenticated.id == user.id
        finally:
            session.close()
    
    def test_jwt_token_generation(self):
        """Test JWT token generation and validation"""
        from backend.auth import AuthenticationManager
        
        user_id = "test_user_123"
        
        # Generate token
        token = AuthenticationManager.create_access_token(user_id)
        assert token is not None
        
        # Verify token
        verified_id = AuthenticationManager.verify_access_token(token)
        assert verified_id == user_id
    
    def test_api_key_generation(self):
        """Test API key generation"""
        from backend.auth import APIKeyManager, UserManager
        from backend.database import db_manager
        
        session = db_manager.get_session()
        try:
            # Create user
            user, _ = UserManager.create_user(
                session=session,
                email="apikey@example.com",
                username="apikeyuser",
                password="password123"
            )
            
            # Generate API key
            api_key = APIKeyManager.create_api_key(
                session=session,
                user_id=user.id,
                name="Test Key",
                rate_limit=100
            )
            
            assert api_key is not None
            assert len(api_key) > 20
        finally:
            session.close()
    
    def test_invalid_credentials(self):
        """Test authentication with invalid credentials"""
        from backend.auth import UserManager
        from backend.database import db_manager
        
        session = db_manager.get_session()
        try:
            # Try to authenticate with wrong password
            result = UserManager.authenticate_user(
                session=session,
                email="nonexistent@example.com",
                password="wrongpassword"
            )
            
            assert result is None
        finally:
            session.close()


# File management tests
class TestFileManagement:
    """Test file management system"""
    
    def test_file_upload(self):
        """Test file upload"""
        from backend.file_manager import get_file_manager
        from werkzeug.datastructures import FileStorage
        from io import BytesIO
        
        file_manager = get_file_manager()
        
        # Create test file
        content = b"def hello(): pass"
        file = FileStorage(
            stream=BytesIO(content),
            filename="test.py",
            content_type="text/plain"
        )
        
        file_id, filename, size, hash_val = file_manager.save_uploaded_file(
            file, 
            user_id="test_user"
        )
        
        assert file_id is not None
        assert filename == "test.py"
        assert size == len(content)
        assert hash_val is not None
    
    def test_file_retrieval(self):
        """Test file retrieval"""
        from backend.file_manager import get_file_manager
        from werkzeug.datastructures import FileStorage
        from io import BytesIO
        
        file_manager = get_file_manager()
        
        # Upload file
        content = b"def hello(): pass"
        file = FileStorage(
            stream=BytesIO(content),
            filename="test.py",
            content_type="text/plain"
        )
        
        file_id, _, _, _ = file_manager.save_uploaded_file(file, user_id="test_user")
        
        # Retrieve file
        retrieved_content = file_manager.read_file_content(file_id)
        assert retrieved_content == content.decode()
    
    def test_file_integrity(self):
        """Test file integrity verification"""
        from backend.file_manager import get_file_manager, CodeDiffGenerator
        import hashlib
        from werkzeug.datastructures import FileStorage
        from io import BytesIO
        
        file_manager = get_file_manager()
        
        # Upload file
        content = b"def hello(): pass"
        file = FileStorage(
            stream=BytesIO(content),
            filename="test.py",
            content_type="text/plain"
        )
        
        file_id, _, _, expected_hash = file_manager.save_uploaded_file(
            file, 
            user_id="test_user"
        )
        
        # Verify integrity
        is_valid = file_manager.verify_file_integrity(file_id, expected_hash)
        assert is_valid is True
    
    def test_code_diff_generation(self):
        """Test code diff generation"""
        from backend.file_manager import CodeDiffGenerator
        
        original = """def calculate(x):
    return x * 2
"""
        
        modified = """def calculate(x):
    return x * 3
"""
        
        diff = CodeDiffGenerator.generate_diff(original, modified)
        assert "3" in diff
        assert "2" in diff


# API Analysis tests
class TestAnalysisAPI:
    """Test analysis submission and retrieval"""
    
    def test_submit_analysis(self):
        """Test analysis submission"""
        from backend.db_models import Analysis
        from backend.database import db_manager
        
        session = db_manager.get_session()
        try:
            analysis = Analysis(
                user_id="test_user",
                file_name="test.py",
                file_size=100,
                file_hash="abc123",
                selected_agents=["security", "performance"]
            )
            
            session.add(analysis)
            session.commit()
            session.refresh(analysis)
            
            assert analysis.id is not None
            assert analysis.status == "SUBMITTED"
        finally:
            session.close()
    
    def test_get_analysis_status(self):
        """Test getting analysis status"""
        from backend.db_models import Analysis
        from backend.database import db_manager
        
        session = db_manager.get_session()
        try:
            # Create analysis
            analysis = Analysis(
                user_id="test_user",
                file_name="test.py",
                file_size=100,
                file_hash="abc123"
            )
            
            session.add(analysis)
            session.commit()
            analysis_id = analysis.id
            
            # Retrieve
            retrieved = session.query(Analysis).get(analysis_id)
            assert retrieved is not None
            assert retrieved.status == "SUBMITTED"
        finally:
            session.close()
    
    def test_update_analysis_results(self):
        """Test updating analysis results"""
        from backend.db_models import Analysis
        from backend.database import db_manager
        import time
        
        session = db_manager.get_session()
        try:
            # Create analysis
            analysis = Analysis(
                user_id="test_user",
                file_name="test.py",
                file_size=100,
                file_hash="abc123"
            )
            
            session.add(analysis)
            session.commit()
            analysis_id = analysis.id
            
            # Update with results
            retrieved = session.query(Analysis).get(analysis_id)
            retrieved.status = "COMPLETED"
            retrieved.quality_score = 85.5
            retrieved.result = {"security": "passed"}
            retrieved.completed_at = datetime.utcnow()
            retrieved.processing_time_ms = 1250
            session.commit()
            
            # Verify update
            final = session.query(Analysis).get(analysis_id)
            assert final.status == "COMPLETED"
            assert final.quality_score == 85.5
        finally:
            session.close()


# Analytics tests
class TestAnalytics:
    """Test analytics system"""
    
    def test_dashboard_stats(self):
        """Test dashboard statistics"""
        from backend.analytics import AnalyticsManager
        from backend.database import db_manager
        from backend.db_models import Analysis
        
        session = db_manager.get_session()
        try:
            user_id = "analytics_test_user"
            
            # Create sample analyses
            for i in range(5):
                analysis = Analysis(
                    user_id=user_id,
                    file_name=f"test{i}.py",
                    file_size=100,
                    quality_score=80 + i
                )
                session.add(analysis)
            
            session.commit()
            
            # Get stats
            stats = AnalyticsManager.get_user_dashboard_stats(session, user_id)
            
            assert stats['total_analyses'] == 5
            assert stats['avg_quality_score'] > 80
        finally:
            session.close()
    
    def test_quality_trend(self):
        """Test quality trend calculation"""
        from backend.analytics import AnalyticsManager
        from backend.database import db_manager
        from backend.db_models import Analysis
        
        session = db_manager.get_session()
        try:
            user_id = "trend_test_user"
            
            # Create analyses over multiple days
            for day in range(5):
                analysis = Analysis(
                    user_id=user_id,
                    file_name=f"test{day}.py",
                    file_size=100,
                    quality_score=70 + day * 5,
                    created_at=datetime.utcnow() - timedelta(days=5-day)
                )
                session.add(analysis)
            
            session.commit()
            
            # Get trend
            trend = AnalyticsManager.get_quality_trend(session, user_id, days=30)
            
            assert trend['trend'] in ['improving', 'degrading', 'stable']
        finally:
            session.close()


# REST API tests
class TestRESTAPI:
    """Test REST API endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        from backend.rest_api_v2 import app
        
        app.config['TESTING'] = True
        
        with app.test_client() as client:
            yield client
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_register_endpoint(self, client):
        """Test user registration endpoint"""
        response = client.post('/auth/register', 
            json={
                'email': 'test@example.com',
                'username': 'testuser',
                'password': 'password123'
            }
        )
        
        assert response.status_code in [201, 200]
        data = json.loads(response.data)
        assert 'access_token' in data
    
    def test_login_endpoint(self, client):
        """Test login endpoint"""
        # First register
        client.post('/auth/register',
            json={
                'email': 'login@example.com',
                'username': 'loginuser',
                'password': 'password123'
            }
        )
        
        # Then login
        response = client.post('/auth/login',
            json={
                'email': 'login@example.com',
                'password': 'password123'
            }
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'access_token' in data
    
    def test_submit_review_endpoint(self, client):
        """Test code review submission"""
        # Register and login first
        user_response = client.post('/auth/register',
            json={
                'email': 'review@example.com',
                'username': 'reviewuser',
                'password': 'password123'
            }
        )
        
        api_key = json.loads(user_response.data)['api_key']
        
        # Submit review
        response = client.post('/review',
            json={
                'code': 'def hello(): pass',
                'agents': ['security']
            },
            headers={'X-API-Key': api_key}
        )
        
        assert response.status_code in [202, 200]
        data = json.loads(response.data)
        assert 'analysis_id' in data


# Integration tests
class TestIntegration:
    """End-to-end integration tests"""
    
    def test_complete_analysis_workflow(self):
        """Test complete analysis workflow"""
        from backend.auth import UserManager, APIKeyManager
        from backend.database import db_manager
        from backend.db_models import Analysis
        from backend.file_manager import get_file_manager
        from werkzeug.datastructures import FileStorage
        from io import BytesIO
        
        session = db_manager.get_session()
        file_manager = get_file_manager()
        
        try:
            # 1. Register user
            user, api_key = UserManager.create_user(
                session=session,
                email="integration@example.com",
                username="integrationuser",
                password="password123"
            )
            
            # 2. Upload file
            content = b"def analyze(): pass"
            file = FileStorage(
                stream=BytesIO(content),
                filename="analyze.py",
                content_type="text/plain"
            )
            
            file_id, _, _, file_hash = file_manager.save_uploaded_file(
                file,
                user_id=user.id
            )
            
            # 3. Create analysis
            analysis = Analysis(
                user_id=user.id,
                file_name="analyze.py",
                file_size=len(content),
                file_hash=file_hash,
                selected_agents=["security", "performance"]
            )
            
            session.add(analysis)
            session.commit()
            session.refresh(analysis)
            
            # 4. Verify analysis created
            assert analysis.id is not None
            assert analysis.status == "SUBMITTED"
            
            # 5. Retrieve analysis
            retrieved = session.query(Analysis).get(analysis.id)
            assert retrieved is not None
            
        finally:
            session.close()


# Performance tests
class TestPerformance:
    """Performance and load tests"""
    
    def test_bulk_analysis_creation(self):
        """Test creating many analyses"""
        from backend.database import db_manager
        from backend.db_models import Analysis
        import time
        
        session = db_manager.get_session()
        
        try:
            start = time.time()
            
            # Create 100 analyses
            for i in range(100):
                analysis = Analysis(
                    user_id="perf_test_user",
                    file_name=f"test_{i}.py",
                    file_size=100,
                    quality_score=80 + (i % 20)
                )
                session.add(analysis)
            
            session.commit()
            
            elapsed = time.time() - start
            
            # Should complete in reasonable time
            assert elapsed < 5.0
        
        finally:
            session.close()
    
    def test_query_performance(self):
        """Test query performance"""
        from backend.database import db_manager
        from backend.db_models import Analysis
        import time
        
        session = db_manager.get_session()
        
        try:
            user_id = "query_test_user"
            
            # Create test data
            for i in range(50):
                analysis = Analysis(
                    user_id=user_id,
                    file_name=f"test_{i}.py",
                    file_size=100,
                    quality_score=70 + (i % 30)
                )
                session.add(analysis)
            
            session.commit()
            
            # Test query performance
            start = time.time()
            
            results = session.query(Analysis).filter(
                Analysis.user_id == user_id
            ).all()
            
            elapsed = time.time() - start
            
            assert len(results) >= 50
            assert elapsed < 1.0  # Should be fast
        
        finally:
            session.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
