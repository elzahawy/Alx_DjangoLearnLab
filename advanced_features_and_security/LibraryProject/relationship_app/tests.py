from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Book, Author, UserProfile

CustomUser = get_user_model()


class CustomUserModelTest(TestCase):
    """Tests for CustomUser model"""
    
    def test_create_user(self):
        """Test creating a regular user"""
        user = CustomUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser(self):
        """Test creating a superuser"""
        user = CustomUser.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class PermissionTest(TestCase):
    """Tests for permissions and groups"""
    
    def setUp(self):
        """Set up test data"""
        self.user = CustomUser.objects.create_user(
            email='user@example.com',
            username='testuser',
            password='testpass123'
        )
        self.content_type = ContentType.objects.get_for_model(Book)
    
    def test_can_view_permission(self):
        """Test can_view permission exists"""
        permission = Permission.objects.get(
            codename='can_view',
            content_type=self.content_type
        )
        self.assertIsNotNone(permission)
    
    def test_permission_required_view(self):
        """Test that views require permissions"""
        # This would require actual view testing
        pass

