"""
Firebase Configuration Module
Provides Firebase initialization and configuration for the application.
This is a stub module - Firebase integration is optional.
"""

import os


class FirebaseConfig:
    """Firebase configuration and initialization class."""
    
    _initialized = False
    _app = None
    
    @classmethod
    def initialize(cls):
        """Initialize Firebase connection."""
        if cls._initialized:
            return cls._app
        
        # Check if Firebase should be used
        use_firebase = os.getenv('USE_FIREBASE', 'False').lower() == 'true'
        
        if not use_firebase:
            print("Firebase disabled - using MySQL database")
            cls._initialized = True
            return None
        
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore
            
            # Get credentials from environment or file
            cred_json = os.getenv('FIREBASE_CREDENTIALS_JSON')
            cred_file = os.getenv('FIREBASE_CREDENTIALS_FILE', 'firebase-credentials.json')
            
            if cred_json:
                import json
                cred_dict = json.loads(cred_json)
                cred = credentials.Certificate(cred_dict)
            elif os.path.exists(cred_file):
                cred = credentials.Certificate(cred_file)
            else:
                print("Warning: No Firebase credentials found")
                cls._initialized = True
                return None
            
            cls._app = firebase_admin.initialize_app(cred)
            cls._initialized = True
            print("Firebase initialized successfully")
            return cls._app
            
        except ImportError:
            print("Warning: firebase-admin not installed")
            cls._initialized = True
            return None
        except Exception as e:
            print(f"Warning: Firebase initialization failed: {e}")
            cls._initialized = True
            return None
    
    @classmethod
    def get_firestore(cls):
        """Get Firestore client."""
        if not cls._initialized:
            cls.initialize()
        
        try:
            from firebase_admin import firestore
            return firestore.client()
        except Exception:
            return None
    
    @classmethod
    def is_available(cls):
        """Check if Firebase is available and initialized."""
        return cls._initialized and cls._app is not None
