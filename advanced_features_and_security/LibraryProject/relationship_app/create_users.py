import os
import django

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Create test users
users_data = [
    {
        'username': 'admin',
        'email': 'admin@library.com',
        'password': 'admin123',
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'username': 'librarian1',
        'email': 'librarian1@library.com',
        'password': 'lib123',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'username': 'librarian2',
        'email': 'librarian2@library.com',
        'password': 'lib123',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'username': 'student1',
        'email': 'student1@library.com',
        'password': 'student123',
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'username': 'student2',
        'email': 'student2@library.com',
        'password': 'student123',
        'is_staff': False,
        'is_superuser': False,
    },
]

print("Creating users...")
print("=" * 60)

created_users = []
for user_data in users_data:
    username = user_data['username']
    # Delete user if exists
    User.objects.filter(username=username).delete()
    
    # Create new user
    user = User.objects.create_user(
        username=username,
        email=user_data['email'],
        password=user_data['password'],
        is_staff=user_data['is_staff'],
        is_superuser=user_data['is_superuser']
    )
    created_users.append({
        'username': username,
        'password': user_data['password'],
        'email': user_data['email'],
        'is_staff': user_data['is_staff'],
        'is_superuser': user_data['is_superuser']
    })
    print(f"✓ Created user: {username}")

print("\n" + "=" * 60)
print("USER LOGIN CREDENTIALS")
print("=" * 60)
print("\n")

for user in created_users:
    user_type = "Admin" if user['is_superuser'] else "Regular User"
    print(f"Username: {user['username']}")
    print(f"Password: {user['password']}")
    print(f"Email: {user['email']}")
    print(f"Type: {user_type}")
    print("-" * 60)

print("\n" + "=" * 60)
print(f"Total users created: {len(created_users)}")
print("=" * 60)
print("\nYou can now login at: http://127.0.0.1:8000/relationship_app/login/")

