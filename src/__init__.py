from flask import Flask, jsonify
from dotenv import load_dotenv
import os
from pathlib import Path

from mwwc_airtable import Airtable
from mwwc_action_network import (
    ActionNetwork,
)
from mwwc_google import (
    GoogleWorkspace,
    get_google_workspace_client,
)

load_dotenv()


def get_project_root() -> Path:
    return Path(__file__).parent.parent


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        AIRTABLE_API_KEY=os.environ["AIRTABLE_API_KEY"],
        AIRTABLE_BASE_ID=os.environ["AIRTABLE_BASE_ID"],
        AIRTABLE_TABLE_ID=os.environ["AIRTABLE_TABLE_ID"],
        AIRTABLE_VIEW_ID=os.environ["AIRTABLE_VIEW_ID"],
        AIRTABLE_CHOSEN_FIRST_NAME=os.environ["AIRTABLE_CHOSEN_FIRST_NAME"],
        AIRTABLE_CHOSEN_LAST_NAME=os.environ["AIRTABLE_CHOSEN_LAST_NAME"],
        AIRTABLE_BU_STATUS=os.environ["AIRTABLE_BU_STATUS"],
        AIRTABLE_AREA=os.environ["AIRTABLE_AREA"],
        AIRTABLE_MIGS=os.environ["AIRTABLE_MIGS"],
        AIRTABLE_STEWARD=os.environ["AIRTABLE_STEWARD"],
        AIRTABLE_AREA_SANTA_FE_LLC=os.environ["AIRTABLE_AREA_SANTA_FE_LLC"],
        AIRTABLE_AREA_SANTA_FE_INC=os.environ["AIRTABLE_AREA_SANTA_FE_INC"],
        AIRTABLE_AREA_DENVER_LLC_GENERAL=os.environ["AIRTABLE_AREA_DENVER_LLC_GENERAL"],
        AIRTABLE_NON_BU_ASSOCIATE=os.environ["AIRTABLE_NON_BU_ASSOCIATE"],
        AIRTABLE_ELECTED_POSITION=os.environ["AIRTABLE_ELECTED_POSITION"],
        AIRTABLE_PERSONAL_EMAIL=os.environ["AIRTABLE_PERSONAL_EMAIL"],
        AIRTABLE_AREA_DENVER_LLC_SECURITY=os.environ["AIRTABLE_AREA_DENVER_LLC_SECURITY"],
        AIRTABLE_GOOGLE_WRITE_PERMISSIONS=os.environ["AIRTABLE_GOOGLE_WRITE_PERMISSIONS"],

        ACTION_NETWORK_BASE_URL=os.environ["ACTION_NETWORK_BASE_URL"],
        ACTION_NETWORK_API_KEY=os.environ["ACTION_NETWORK_API_KEY"],
    )

    @app.route("/")
    def index():
        return f"""
        {__name__}
        <p>The UI goes here.</p><p>{os.getenv('TEST_VAR', 'default')}</p>
        """

    @app.route("/sync-contacts")
    def sync_contacts():
        return {}

    @app.route("/restore-backup")
    def restore_backup():
        return {}

    @app.route("/scratch/airtable")
    def scratch_airtable():
        airtable = Airtable(app.config)
        airtable.get_banana_data()
        differences = airtable.get_differences()
        return jsonify(differences)
        # return jsonify(airtable.banana_data)

    @app.route("/scratch/action-network")
    def scratch_action_network():
        try:
            client = ActionNetwork((app.config))
            people = client.get_people()

            return jsonify(people)

        except Exception as e:
            message = {"error": f"An error occurred: {e}"}
            return jsonify(message)

    @app.route("/scratch/google")
    def scratch_google():
        try:
            airtable = Airtable(app.config)
            airtable.get_banana_data()
            differences = airtable.get_differences()

            # TODO: Clean this up
            if differences is not None:
                additions = differences.get("additions", [])
                deletions = differences.get("deletions", [])
            else:
                additions = []
                deletions = []

            google_client = get_google_workspace_client()

            google = GoogleWorkspace(google_client, additions, deletions)
            return jsonify(google.groups)

        except Exception as e:
            message = {"error": f"An http error occurred: {e}"}
            return jsonify(message)

    return app
