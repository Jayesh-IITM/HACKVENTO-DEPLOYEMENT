"""
Firebase Adapter Module
Provides data access methods for Firebase Firestore.
This is a stub module - Firebase integration is optional.
"""

from firebase_config import FirebaseConfig


class FirebaseAdapter:
    """Adapter class for Firebase Firestore operations."""
    
    def __init__(self):
        """Initialize the Firebase adapter."""
        self.db = FirebaseConfig.get_firestore()
    
    def _get_collection(self, name):
        """Get a Firestore collection reference."""
        if self.db is None:
            return None
        return self.db.collection(name)
    
    # ==================== User Methods ====================
    
    def get_user(self, user_id):
        """Get user by ID."""
        users = self._get_collection('users')
        if users is None:
            return None
        doc = users.document(str(user_id)).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def get_user_by_email(self, email):
        """Get user by email."""
        users = self._get_collection('users')
        if users is None:
            return None
        query = users.where('email', '==', email).limit(1).get()
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def create_user(self, email, password_hash, role_id, is_verified=False):
        """Create a new user."""
        users = self._get_collection('users')
        if users is None:
            return None
        doc_ref = users.document()
        doc_ref.set({
            'email': email,
            'password_hash': password_hash,
            'role_id': role_id,
            'is_verified': is_verified,
            'created_at': FirebaseConfig.get_firestore().SERVER_TIMESTAMP if self.db else None
        })
        return doc_ref.id
    
    def update_user(self, user_id, data):
        """Update user data."""
        users = self._get_collection('users')
        if users is None:
            return False
        users.document(str(user_id)).update(data)
        return True
    
    # ==================== Student Methods ====================
    
    def get_student(self, student_id):
        """Get student by ID."""
        students = self._get_collection('students')
        if students is None:
            return None
        doc = students.document(str(student_id)).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def get_student_by_user_id(self, user_id):
        """Get student by user ID."""
        students = self._get_collection('students')
        if students is None:
            return None
        query = students.where('user_id', '==', str(user_id)).limit(1).get()
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def create_student(self, user_id, data):
        """Create a new student."""
        students = self._get_collection('students')
        if students is None:
            return None
        doc_ref = students.document()
        student_data = {**data, 'user_id': str(user_id)}
        doc_ref.set(student_data)
        return doc_ref.id
    
    def update_student(self, student_id, data):
        """Update student data."""
        students = self._get_collection('students')
        if students is None:
            return False
        students.document(str(student_id)).update(data)
        return True
    
    # ==================== Company Methods ====================
    
    def get_company(self, company_id):
        """Get company by ID."""
        companies = self._get_collection('companies')
        if companies is None:
            return None
        doc = companies.document(str(company_id)).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def get_company_by_user_id(self, user_id):
        """Get company by user ID."""
        companies = self._get_collection('companies')
        if companies is None:
            return None
        query = companies.where('user_id', '==', str(user_id)).limit(1).get()
        for doc in query:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    def create_company(self, user_id, data):
        """Create a new company."""
        companies = self._get_collection('companies')
        if companies is None:
            return None
        doc_ref = companies.document()
        company_data = {**data, 'user_id': str(user_id)}
        doc_ref.set(company_data)
        return doc_ref.id
    
    def update_company(self, company_id, data):
        """Update company data."""
        companies = self._get_collection('companies')
        if companies is None:
            return False
        companies.document(str(company_id)).update(data)
        return True
    
    # ==================== Job Methods ====================
    
    def get_jobs(self, filters=None):
        """Get jobs with optional filters."""
        jobs = self._get_collection('jobs')
        if jobs is None:
            return []
        query = jobs
        if filters:
            for key, value in filters.items():
                query = query.where(key, '==', value)
        return [{'id': doc.id, **doc.to_dict()} for doc in query.get()]
    
    def get_job(self, job_id):
        """Get job by ID."""
        jobs = self._get_collection('jobs')
        if jobs is None:
            return None
        doc = jobs.document(str(job_id)).get()
        if doc.exists:
            data = doc.to_dict()
            data['id'] = doc.id
            return data
        return None
    
    # ==================== Application Methods ====================
    
    def get_applications(self, filters=None):
        """Get applications with optional filters."""
        applications = self._get_collection('applications')
        if applications is None:
            return []
        query = applications
        if filters:
            for key, value in filters.items():
                query = query.where(key, '==', value)
        return [{'id': doc.id, **doc.to_dict()} for doc in query.get()]
    
    def create_application(self, data):
        """Create a new application."""
        applications = self._get_collection('applications')
        if applications is None:
            return None
        doc_ref = applications.document()
        doc_ref.set(data)
        return doc_ref.id
