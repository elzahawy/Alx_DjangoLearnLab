"""
Task 1: Script to set up Groups and Permissions
Run this script to create groups (Editors, Viewers, Admins) and assign permissions.

Usage:
    python manage.py shell < setup_groups.py
    OR
    python manage.py shell
    >>> exec(open('LibraryProject/relationship_app/setup_groups.py').read())
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from LibraryProject.relationship_app.models import Book

# Get content type for Book model
content_type = ContentType.objects.get_for_model(Book)

# Get permissions from Book model
can_view = Permission.objects.get(codename='can_view', content_type=content_type)
can_create = Permission.objects.get(codename='can_create', content_type=content_type)
can_edit = Permission.objects.get(codename='can_edit', content_type=content_type)
can_delete = Permission.objects.get(codename='can_delete', content_type=content_type)

# Create or get groups
editors_group, created = Group.objects.get_or_create(name='Editors')
if created:
    editors_group.permissions.add(can_create, can_edit)
    print("Created 'Editors' group with can_create and can_edit permissions")
else:
    print("'Editors' group already exists")

viewers_group, created = Group.objects.get_or_create(name='Viewers')
if created:
    viewers_group.permissions.add(can_view)
    print("Created 'Viewers' group with can_view permission")
else:
    print("'Viewers' group already exists")

admins_group, created = Group.objects.get_or_create(name='Admins')
if created:
    admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
    print("Created 'Admins' group with all permissions")
else:
    print("'Admins' group already exists")

print("\nGroups setup complete!")
print("\nGroup Permissions:")
print(f"Editors: {[p.codename for p in editors_group.permissions.all()]}")
print(f"Viewers: {[p.codename for p in viewers_group.permissions.all()]}")
print(f"Admins: {[p.codename for p in admins_group.permissions.all()]}")

