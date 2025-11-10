# Advanced Features and Security - Django Project

This project implements advanced Django features including custom user models, role-based access control, permissions, groups, and security best practices.

## Project Structure

```
advanced_features_and_security/
├── LibraryProject/
│   ├── relationship_app/
│   │   ├── models.py          # Custom User Model, Book permissions
│   │   ├── views.py           # Permission-protected views
│   │   ├── admin.py           # Custom User Admin
│   │   ├── urls.py            # URL patterns
│   │   ├── signals.py         # Auto-create UserProfile
│   │   └── templates/
│   ├── settings.py            # Security configurations
│   └── urls.py
└── manage.py
```

## Task 0: Custom User Model

### Implementation
- **CustomUser Model**: Extends `AbstractUser` with:
  - `email` as the USERNAME_FIELD (unique)
  - `date_of_birth` (DateField)
  - `profile_photo` (ImageField)
- **CustomUserManager**: Handles user creation with `create_user()` and `create_superuser()`
- **AUTH_USER_MODEL**: Set to `'relationship_app.CustomUser'` in settings.py
- **Admin Integration**: CustomUserAdmin configured with all fields

### Usage
```python
from relationship_app.models import CustomUser

# Create user
user = CustomUser.objects.create_user(
    email='user@example.com',
    username='user',
    password='password123',
    date_of_birth='1990-01-01'
)
```

## Task 1: Managing Permissions and Groups

### Step 1: Define Custom Permissions in Models
The Book model in `bookshelf/models.py` includes the following custom permissions:
- `can_view` - Permission to view books
- `can_create` - Permission to create books
- `can_edit` - Permission to edit books
- `can_delete` - Permission to delete books

These permissions are defined in the Book model's Meta class:
```python
class Meta:
    permissions = [
        ('can_view', 'Can view book'),
        ('can_create', 'Can create book'),
        ('can_edit', 'Can edit book'),
        ('can_delete', 'Can delete book'),
    ]
```

### Step 2: Create and Configure Groups with Assigned Permissions
Three groups are configured:
1. **Editors**: Have `can_create` and `can_edit` permissions
2. **Viewers**: Have `can_view` permission only
3. **Admins**: Have all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`)

Groups can be created via Django Admin or using the `setup_groups.py` script.

### Setting Up Groups (via Django Admin or Shell)

#### Via Django Admin:
1. Go to `/admin/auth/group/`
2. Create groups: Editors, Viewers, Admins
3. Assign permissions to each group

#### Via Django Shell:
```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from LibraryProject.bookshelf.models import Book

# Get content type for Book model
content_type = ContentType.objects.get_for_model(Book)

# Get permissions
can_view = Permission.objects.get(codename='can_view', content_type=content_type)
can_create = Permission.objects.get(codename='can_create', content_type=content_type)
can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

# Create Editors group
editors_group = Group.objects.create(name='Editors')
editors_group.permissions.add(can_create, can_edit)

# Create Viewers group
viewers_group = Group.objects.create(name='Viewers')
viewers_group.permissions.add(can_view)

# Create Admins group
admins_group = Group.objects.create(name='Admins')
admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
```

### Assigning Users to Groups
```python
from relationship_app.models import CustomUser
from django.contrib.auth.models import Group

user = CustomUser.objects.get(email='user@example.com')
editors_group = Group.objects.get(name='Editors')
user.groups.add(editors_group)
```

### Step 3: Enforce Permissions in Views
Views are modified to check for permissions before allowing users to perform certain actions. The `@permission_required` decorator is used to enforce these permissions.

Views with Permission Checks:
- `list_books()` - Requires `bookshelf.can_view` permission
- `view_book()` - Requires `bookshelf.can_view` permission
- `add_book()` - Requires `bookshelf.can_create` permission
- `edit_book()` - Requires `bookshelf.can_edit` permission
- `delete_book()` - Requires `bookshelf.can_delete` permission

All views use `@permission_required` decorator with `raise_exception=True`.

Example:
```python
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # View implementation
```

## Task 2: Security Best Practices

### Security Settings Configured
1. **DEBUG**: Set to `False` for production
2. **SECURE_BROWSER_XSS_FILTER**: `True` - Enables browser XSS filtering
3. **X_FRAME_OPTIONS**: `'DENY'` - Prevents clickjacking
4. **SECURE_CONTENT_TYPE_NOSNIFF**: `True` - Prevents MIME-sniffing
5. **CSRF Protection**: All forms include `{% csrf_token %}`

### Secure Data Access
- All views use Django ORM (no raw SQL)
- User input is validated and sanitized
- `get_object_or_404()` used for safe object retrieval
- Search functionality uses Django ORM Q objects (prevents SQL injection)

### CSRF Protection
All form templates include:
```django
{% csrf_token %}
```

## Task 3: HTTPS and Secure Redirects

### HTTPS Configuration
1. **SECURE_SSL_REDIRECT**: `True` - Redirects HTTP to HTTPS
2. **SECURE_HSTS_SECONDS**: `31536000` (1 year)
3. **SECURE_HSTS_INCLUDE_SUBDOMAINS**: `True`
4. **SECURE_HSTS_PRELOAD**: `True`

### Secure Cookies
1. **SESSION_COOKIE_SECURE**: `True` - Session cookies only over HTTPS
2. **CSRF_COOKIE_SECURE**: `True` - CSRF cookies only over HTTPS

### Secure Headers
- **X_FRAME_OPTIONS**: `'DENY'`
- **SECURE_CONTENT_TYPE_NOSNIFF**: `True`
- **SECURE_BROWSER_XSS_FILTER**: `True`

### Deployment Notes
For development without HTTPS, set:
- `SECURE_SSL_REDIRECT = False`
- `SESSION_COOKIE_SECURE = False`
- `CSRF_COOKIE_SECURE = False`

For production with HTTPS, ensure:
- SSL/TLS certificate is configured on your web server (Nginx/Apache)
- All security settings are set to `True`
- `ALLOWED_HOSTS` is configured with your domain

## Testing Permissions

### Create Test Users
```python
from relationship_app.models import CustomUser
from django.contrib.auth.models import Group

# Create users
editor_user = CustomUser.objects.create_user(
    email='editor@example.com',
    username='editor',
    password='password123'
)

viewer_user = CustomUser.objects.create_user(
    email='viewer@example.com',
    username='viewer',
    password='password123'
)

# Assign to groups
editors_group = Group.objects.get(name='Editors')
viewers_group = Group.objects.get(name='Viewers')

editor_user.groups.add(editors_group)
viewer_user.groups.add(viewers_group)
```

### Test Access
1. Log in as `editor@example.com` - Should be able to create and edit books
2. Log in as `viewer@example.com` - Should only be able to view books
3. Attempt to access restricted views - Should receive permission denied errors

## Running the Project

1. **Create migrations**:
   ```bash
   python manage.py makemigrations
   ```

2. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run server**:
   ```bash
   python manage.py runserver
   ```

## Important Notes

- **Custom User Model**: Must be set before first migration. If you need to change it later, you'll need to recreate the database.
- **Permissions**: Run migrations after adding custom permissions to make them available in Django admin.
- **HTTPS Settings**: Some settings may cause issues in development. Adjust as needed for your environment.

