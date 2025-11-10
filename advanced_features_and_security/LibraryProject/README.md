# Managing Permissions and Groups in Django

This document explains how permissions and groups are configured and used in this Django application.

## Step 1: Define Custom Permissions in Models

Custom permissions have been added to the `Book` model in `bookshelf/models.py` to control actions such as viewing, creating, editing, or deleting instances of that model.

### Permissions Defined

The Book model includes the following custom permissions:
- `can_view` - Permission to view books
- `can_create` - Permission to create books
- `can_edit` - Permission to edit books
- `can_delete` - Permission to delete books

These permissions are defined in the Book model's Meta class:

```python
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    class Meta:
        permissions = [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]
```

## Step 2: Create and Configure Groups with Assigned Permissions

User groups have been set up in Django with the newly created permissions assigned to these groups. Groups can be managed through Django's admin site.

### Groups Setup

Three groups are configured:
1. **Editors**: Have `can_create` and `can_edit` permissions
2. **Viewers**: Have `can_view` permission only
3. **Admins**: Have all permissions (`can_view`, `can_create`, `can_edit`, `can_delete`)

### Setting Up Groups

#### Via Django Admin:
1. Go to `/admin/auth/group/`
2. Create groups: Editors, Viewers, Admins
3. Assign appropriate permissions to each group

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
from LibraryProject.bookshelf.models import CustomUser
from django.contrib.auth.models import Group

user = CustomUser.objects.get(email='user@example.com')
editors_group = Group.objects.get(name='Editors')
user.groups.add(editors_group)
```

## Step 3: Enforce Permissions in Views

Views have been modified to check for these permissions before allowing users to perform certain actions. The `@permission_required` decorator is used to enforce these permissions.

### Views with Permission Checks

Views that create, edit, or delete model instances check for the correct permissions:

- `book_list()` - Requires `bookshelf.can_view` permission
- `view_book()` - Requires `bookshelf.can_view` permission
- `add_book()` - Requires `bookshelf.can_create` permission
- `edit_book()` - Requires `bookshelf.can_edit` permission
- `delete_book()` - Requires `bookshelf.can_delete` permission

### Example Implementation

All views use `@permission_required` decorator with `raise_exception=True`:

```python
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    # View implementation
    pass

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    # View implementation
    pass
```

## Step 4: Test Permissions

To test the implementation:

1. Create test users and assign them to different groups
2. Log in as these users
3. Attempt to access various parts of the application
4. Verify that permissions are applied correctly

### Testing Approach

1. Create a user and assign them to the "Viewers" group
2. Log in as that user
3. Try to access the book list - should work (has can_view)
4. Try to add a book - should fail (doesn't have can_create)
5. Create another user and assign them to the "Editors" group
6. Log in as that user
7. Try to add/edit books - should work (has can_create and can_edit)
8. Try to delete a book - should fail (doesn't have can_delete)

## Summary

This application implements a comprehensive permissions and groups system:

- **Custom Permissions**: Defined in the Book model (can_view, can_create, can_edit, can_delete)
- **Groups**: Three groups (Editors, Viewers, Admins) with appropriate permissions
- **View Protection**: All views use `@permission_required` decorator with `raise_exception=True`
- **Testing**: Manual testing can be performed by creating users and assigning them to groups

For more information, see the main README.md in the project root.

