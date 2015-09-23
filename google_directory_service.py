"""Module to interact with Google Directory API."""

from apiclient.discovery import build


MY_CUSTOMER_ALIAS = 'my_customer'

NUM_RETRIES = 3


class GoogleDirectoryService(object):
  """Interact with Google Directory API."""

  def __init__(self, oauth_decorator):
    self.service = build(serviceName='admin',
                         version='directory_v1',
                         http=oauth_decorator.http())

  def GetUsers(self):
    """Get the users of a customer account.

    Returns:
      users: A list of users.
    """
    users = []
    page_token = ''
    while True:
      request = self.service.users().list(customer=MY_CUSTOMER_ALIAS,
                                          maxResults=500,
                                          pageToken=page_token,
                                          projection='full',
                                          orderBy='email')
      result = request.execute(num_retries=NUM_RETRIES)
      users += result['users']
      if 'nextPageToken' in result:
        page_token = result['nextPageToken']
      else:
        break

    return users