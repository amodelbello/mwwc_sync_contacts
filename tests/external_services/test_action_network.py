import sys
import requests
from mwwc_sync_contacts.external_services.action_network import ActionNetwork


sys.path.append("...")


config_fixture = {
    "ACTION_NETWORK_API_KEY": "api_key",
    "ACTION_NETWORK_BASE_URL": "base_url",
}


def test_get_people(
    monkeypatch,
    action_network_people,
    action_network_people_no_next,
):
    class MockResponse:
        num_requests = 0

        @staticmethod
        def json():
            if MockResponse.num_requests < 3:
                MockResponse.num_requests += 1
                return action_network_people
            else:
                return action_network_people_no_next

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    action_network = ActionNetwork(config_fixture)
    people = action_network.get_people()
    print(people)
    assert people is not None
