"""
AgentMesh Python SDK
Client library for interacting with AgentMesh REST API
"""
import requests
import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path
import hashlib


class AgentMeshAPIError(Exception):
    """Base exception for API errors"""
    pass


class AuthenticationError(AgentMeshAPIError):
    """Authentication failed"""
    pass


class ValidationError(AgentMeshAPIError):
    """Request validation failed"""
    pass


class AgentMeshAPI:
    """Python SDK for AgentMesh REST API"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        access_token: Optional[str] = None,
        base_url: str = "http://localhost:5000",
        timeout: int = 30
    ):
        """
        Initialize AgentMesh API client
        
        Args:
            api_key: API key for authentication
            access_token: JWT access token for authentication
            base_url: Base URL of the API server
            timeout: Request timeout in seconds
        """
        self.api_key = api_key
        self.access_token = access_token
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
    
    def _get_headers(self, content_type: str = "application/json") -> Dict[str, str]:
        """Build request headers"""
        headers = {"Content-Type": content_type}
        
        if self.api_key:
            headers["X-API-Key"] = self.api_key
        elif self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        return headers
    
    def _request(
        self,
        method: str,
        endpoint: str,
        json_data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
        content_type: Optional[str] = None
    ) -> Any:
        """Make HTTP request"""
        url = f"{self.base_url}{endpoint}"
        
        headers = self._get_headers(content_type or "application/json")
        if files:
            # Remove Content-Type for multipart/form-data
            headers.pop("Content-Type", None)
        
        try:
            response = self.session.request(
                method,
                url,
                json=json_data,
                files=files,
                params=params,
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code >= 400:
                error_data = response.json() if response.text else {}
                error_msg = error_data.get('error', f"HTTP {response.status_code}")
                
                if response.status_code == 401:
                    raise AuthenticationError(error_msg)
                elif response.status_code == 400:
                    raise ValidationError(error_msg)
                else:
                    raise AgentMeshAPIError(error_msg)
            
            return response.json() if response.text else {}
        
        except requests.RequestException as e:
            raise AgentMeshAPIError(f"Request failed: {str(e)}")
    
    # ============================================================
    # Authentication Methods
    # ============================================================
    
    def register(
        self,
        email: str,
        username: str,
        password: str
    ) -> Dict[str, Any]:
        """Register new user"""
        data = {
            "email": email,
            "username": username,
            "password": password
        }
        
        result = self._request("POST", "/auth/register", json_data=data)
        
        # Store tokens for future requests
        self.access_token = result.get('access_token')
        self.api_key = result.get('api_key')
        
        return result
    
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        data = {"email": email, "password": password}
        
        result = self._request("POST", "/auth/login", json_data=data)
        
        # Store token for future requests
        self.access_token = result.get('access_token')
        
        return result
    
    def validate_token(self) -> Dict[str, Any]:
        """Validate current token"""
        return self._request("GET", "/auth/validate-token")
    
    # ============================================================
    # API Key Methods
    # ============================================================
    
    def generate_api_key(
        self,
        name: str,
        rate_limit: int = 100
    ) -> str:
        """Generate new API key"""
        data = {"name": name, "rate_limit": rate_limit}
        
        result = self._request("POST", "/api-keys/generate", json_data=data)
        
        api_key = result.get('api_key')
        self.api_key = api_key
        
        return api_key
    
    def list_api_keys(self) -> List[Dict[str, Any]]:
        """List user's API keys"""
        result = self._request("GET", "/api-keys")
        return result.get('api_keys', [])
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke API key"""
        try:
            self._request("DELETE", f"/api-keys/{key_id}")
            return True
        except AgentMeshAPIError:
            return False
    
    # ============================================================
    # Code Analysis Methods
    # ============================================================
    
    def submit_analysis(
        self,
        code: Optional[str] = None,
        file_path: Optional[str] = None,
        description: Optional[str] = None,
        agents: Optional[List[str]] = None,
        priority: str = "MEDIUM"
    ) -> Dict[str, Any]:
        """Submit code for analysis"""
        if not code and not file_path:
            raise ValidationError("Either code or file_path must be provided")
        
        if file_path:
            with open(file_path, 'r') as f:
                code = f.read()
        
        data = {
            "code": code,
            "description": description or "Code review",
            "agents": agents or ["security", "code_quality"],
            "priority": priority
        }
        
        if file_path:
            data["file_name"] = Path(file_path).name
        
        return self._request("POST", "/review", json_data=data)
    
    def get_analysis(self, analysis_id: str) -> Dict[str, Any]:
        """Get analysis results"""
        return self._request("GET", f"/analyses/{analysis_id}")
    
    def list_analyses(
        self,
        limit: int = 50,
        status: Optional[str] = None
    ) -> Dict[str, Any]:
        """List analyses"""
        params = {"limit": limit}
        if status:
            params["status"] = status
        
        return self._request("GET", "/analyses", params=params)
    
    def wait_for_analysis(
        self,
        analysis_id: str,
        max_wait: int = 300,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """
        Wait for analysis to complete
        
        Args:
            analysis_id: ID of analysis to wait for
            max_wait: Maximum wait time in seconds
            poll_interval: Polling interval in seconds
        
        Returns:
            Analysis result
        
        Raises:
            TimeoutError: If analysis doesn't complete within max_wait
        """
        start_time = time.time()
        
        while True:
            analysis = self.get_analysis(analysis_id)
            
            if analysis['status'] in ['COMPLETED', 'FAILED']:
                return analysis
            
            if time.time() - start_time > max_wait:
                raise TimeoutError(f"Analysis did not complete within {max_wait} seconds")
            
            time.sleep(poll_interval)
    
    # ============================================================
    # Report Methods
    # ============================================================
    
    def generate_report(
        self,
        analysis_id: str,
        format: str = "json",
        template: str = "default",
        save_path: Optional[str] = None
    ) -> Any:
        """
        Generate report for analysis
        
        Args:
            analysis_id: ID of analysis
            format: Report format (json, html, pdf)
            template: Report template (default, executive, detailed)
            save_path: Path to save report file (for pdf/html)
        
        Returns:
            Report data (dict for JSON) or bytes (for pdf/html)
        """
        data = {"format": format, "template": template}
        
        try:
            response = self.session.post(
                f"{self.base_url}/reports/{analysis_id}",
                json=data,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code >= 400:
                raise AgentMeshAPIError(f"Report generation failed: {response.status_code}")
            
            if format == "json":
                return response.json()
            else:  # pdf or html
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    return f"Report saved to {save_path}"
                return response.content
        
        except requests.RequestException as e:
            raise AgentMeshAPIError(f"Report request failed: {str(e)}")
    
    # ============================================================
    # File Methods
    # ============================================================
    
    def upload_file(self, file_path: str) -> Dict[str, Any]:
        """Upload file for analysis"""
        if not Path(file_path).exists():
            raise ValidationError(f"File not found: {file_path}")
        
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return self._request("POST", "/upload", files=files)
    
    def get_file(self, file_id: str) -> str:
        """Get uploaded file content"""
        result = self._request("GET", f"/files/{file_id}")
        return result.get('content', '')
    
    # ============================================================
    # Analytics Methods
    # ============================================================
    
    def get_dashboard_analytics(self) -> Dict[str, Any]:
        """Get user dashboard analytics"""
        return self._request("GET", "/analytics/dashboard")
    
    def get_quality_trends(self, days: int = 30) -> Dict[str, Any]:
        """Get quality trends"""
        params = {"days": days}
        return self._request("GET", "/analytics/trends", params=params)
    
    def get_comprehensive_analytics(self) -> Dict[str, Any]:
        """Get comprehensive analytics"""
        return self._request("GET", "/analytics/comprehensive")
    
    # ============================================================
    # Notification Methods
    # ============================================================
    
    def get_notifications(
        self,
        unread_only: bool = False,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get user notifications"""
        params = {"unread": unread_only, "limit": limit}
        result = self._request("GET", "/notifications", params=params)
        return result.get('notifications', [])
    
    # ============================================================
    # System Methods
    # ============================================================
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        return self._request("GET", "/health")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return self._request("GET", "/system/stats")
    
    # ============================================================
    # Batch Methods
    # ============================================================
    
    def batch_analyze(
        self,
        files: List[str],
        agents: Optional[List[str]] = None,
        wait: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Analyze multiple files
        
        Args:
            files: List of file paths
            agents: Agents to use for analysis
            wait: Wait for all analyses to complete
        
        Returns:
            List of analysis results
        """
        results = []
        
        for file_path in files:
            try:
                result = self.submit_analysis(
                    file_path=file_path,
                    agents=agents
                )
                
                if wait:
                    result = self.wait_for_analysis(result['analysis_id'])
                
                results.append(result)
            
            except Exception as e:
                results.append({
                    'file': file_path,
                    'error': str(e)
                })
        
        return results
    
    def batch_report(
        self,
        analysis_ids: List[str],
        format: str = "json",
        template: str = "default"
    ) -> List[Any]:
        """Generate reports for multiple analyses"""
        reports = []
        
        for analysis_id in analysis_ids:
            try:
                report = self.generate_report(
                    analysis_id,
                    format=format,
                    template=template
                )
                reports.append(report)
            
            except Exception as e:
                reports.append({
                    'analysis_id': analysis_id,
                    'error': str(e)
                })
        
        return reports


class AsyncAgentMeshAPI(AgentMeshAPI):
    """Async version of AgentMesh API client (experimental)"""
    
    async def submit_analysis_async(
        self,
        code: Optional[str] = None,
        file_path: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Submit analysis asynchronously"""
        # Implementation for async support
        pass


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = AgentMeshAPI(
        api_key="sk_live_...",
        base_url="http://localhost:5000"
    )
    
    # Submit code for analysis
    result = client.submit_analysis(
        code="""
def calculate_discount(price, discount_percent):
    return price * (1 - discount_percent / 100)
""",
        agents=["security", "performance", "code_quality"],
        priority="HIGH"
    )
    
    print(f"Analysis ID: {result['analysis_id']}")
    
    # Wait for analysis to complete
    analysis = client.wait_for_analysis(result['analysis_id'])
    print(f"Quality Score: {analysis['quality_score']}")
    print(f"Final Decision: {analysis['final_decision']}")
    
    # Generate report
    report = client.generate_report(
        analysis['id'],
        format='pdf',
        save_path='report.pdf'
    )
    print(f"Report: {report}")
    
    # Get analytics
    analytics = client.get_dashboard_analytics()
    print(f"Total Analyses: {analytics['total_analyses']}")
    print(f"Average Quality Score: {analytics['avg_quality_score']}")
