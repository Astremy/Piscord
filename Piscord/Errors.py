class Error(Exception):

	def __str__(self):
		return f"Unknown Error"

class PermissionsError(Error):

	def __str__(self):
		return f"You do not have permission to do this action"

class BadRequestError(Error):

	def __str__(self):
		return f"Your query was incomplete or bad"