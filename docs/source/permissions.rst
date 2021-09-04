Permissions
-----------

The permissions of any thing in piscord

List of permissions
^^^^^^^^^^^^^^^^^^^

.. automodule:: piscord.Permission
	:no-undoc-members:

Use Permission
^^^^^^^^^^^^^^

You can use permission to do operations.

1. You can verify permission

.. code-block:: python

	if role.permissions == Permission.ADMINISTRATOR:
		...

2. You can add a permission

.. code-block:: python

	role.permissions += Permission.CHANGE_NICKNAME
	role.edit(permissions = role.permissions)

	# ---------------
	
	perm = channel.permission_overwrites
	perm.edit(deny = perm.deny + Permission.SEND_MESSAGES)

3. You can remove a permission

.. code-block:: python

	role.permissions -= Permission.CHANGE_NICKNAME
	role.edit(permissions = role.permissions)

	# ---------------
	
	perm = channel.permission_overwrites
	perm.edit(deny = perm.deny - Permission.SEND_MESSAGES)