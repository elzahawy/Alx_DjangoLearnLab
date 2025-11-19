# Django Permissions and Groups

This project uses Django groups and custom permissions to control access.

## Custom Permissions
Defined inside LibraryProject/bookshelf/models.py under the Book model:
- can_view
- can_create
- can_edit
- can_delete

## Groups
Groups created in admin:
- Viewers → can_view
- Editors → can_view, can_create, can_edit
- Admins → all permissions

## Permission Usage in Views
Views are protected with decorators such as:
@permission_required('bookshelf.can_create', raise_exception=True)

## Testing
Users are added to groups in admin, and each permission is tested by logging in and attempting to access restricted views.
