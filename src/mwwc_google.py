from __future__ import print_function
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from from_root import from_root

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/admin.directory.group",
    "https://www.googleapis.com/auth/admin.directory.group.member",
    "https://www.googleapis.com/auth/admin.directory.rolemanagement",
    "https://www.googleapis.com/auth/admin.directory.user.security",
]


def get_google_workspace_client():  # pragma: no cover
    """
    This is google provided code to instantiate its python client
    # TODO: Consider moving this to it's own file
    """
    creds = None
    path = from_root() / "gcp_creds"
    token_file = path / "token.json"
    credentials_file = path / "credentials.json"

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file,
                SCOPES,
            )
            creds = flow.run_local_server(port=8000)

        # Save the credentials for the next run
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    client = build("admin", "directory_v1", credentials=creds)
    return client


class GoogleWorkspace():
    def __init__(self, client, additions=[], deletions=[]):
        self.client = client
        self.additions = additions
        self.deletions = deletions
        self._groups = None

    def _get_groups(self):
        groups_result = (
            self.client.groups()
            .list(customer="my_customer", maxResults=100, orderBy="email")
            .execute()
        )
        return groups_result.get("groups", [])

    @property
    def groups(self):
        if self._groups is None:
            self._groups = self._get_groups()
        return self._groups

    def remove_members():
        # foreach groups
        #    foreach members
        #       try remove member
        #       catch continue
        pass

    def add_members():
        pass

    def sync_google_workspace(client):
        # Try to add member
        # member = {
        #     "email": "sync_test@hello.com",
        #     "role": "MEMBER",
        # }

        # add a member to a group (this is all-bu)
        # client.members().insert(groupKey="01d96cc0179jnck", body=member).execute()

        # remove a member from a group
        # client.members().delete(
        #     groupKey="01d96cc0179jnck", memberKey="amodelbello+mwwc_test@pm.me"
        # ).execute()

        # won't work. we don't have an enterprise account
        # is_in_group = client.members().hasMember(
        #     groupKey="01d96cc0179jnck", memberKey="sync_test@hello.com"
        # ).execute()
        # print(f"is in group?: {is_in_group.isMember}")

        members = []

        # list(groupKey, includeDerivedMembership=None, maxResults=None, pageToken=None, roles=None, x__xgafv=None)
        # for i, group in enumerate(groups):
        #     members_result = (
        #         client.members()
        #         .list(
        #             groupKey=group["email"],
        #             maxResults=10,
        #             # pageToken=str(i),
        #             # roles="MEMBER",
        #         )
        #         .execute()
        #     )
        #     members.append(members_result.get("members", []))
        # break
        members_result = (
            client.members()
            .list(
                groupKey="all-bu@meowwolfworkers.org",
                # maxResults=200,
            )
            .execute()
        )
        members = members_result.get("members", [])

        # privs_result = (
        #     client.privileges()
        #     .list(
        #         customer="my_customer",
        #     )
        #     .execute()
        # )
        # privs = privs_result.get("items", [])

        if not members:
            print("No users in the domain.")
            # return privs
        else:
            return members
            # response = []
            # for group in groups:
            #     full_name = group["name"]["fullName"]
            #     response.append("{0} ({1})".format(group["primaryEmail"], full_name))
            # return response
