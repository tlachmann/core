"""Tests for Steam integration."""
from unittest.mock import patch

from homeassistant.components.steam_online import DOMAIN
from homeassistant.components.steam_online.const import CONF_ACCOUNT, CONF_ACCOUNTS
from homeassistant.const import CONF_API_KEY, CONF_NAME
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry

API_KEY = "abc123"
ACCOUNT_1 = "1234567890"
ACCOUNT_2 = "1234567891"
ACCOUNT_NAME_1 = "testaccount1"
ACCOUNT_NAME_2 = "testaccount2"

CONF_DATA = {
    CONF_API_KEY: API_KEY,
    CONF_ACCOUNT: ACCOUNT_1,
}

CONF_OPTIONS = {
    CONF_ACCOUNTS: {
        ACCOUNT_1: {
            CONF_NAME: ACCOUNT_NAME_1,
            "enabled": True,
        }
    }
}

CONF_OPTIONS_2 = {
    CONF_ACCOUNTS: {
        ACCOUNT_1: {
            CONF_NAME: ACCOUNT_NAME_1,
            "enabled": True,
        },
        ACCOUNT_2: {
            CONF_NAME: ACCOUNT_NAME_2,
            "enabled": True,
        },
    }
}

CONF_IMPORT_OPTIONS = {
    CONF_ACCOUNTS: {
        ACCOUNT_1: {
            CONF_NAME: ACCOUNT_NAME_1,
            "enabled": True,
        },
        ACCOUNT_2: {
            CONF_NAME: ACCOUNT_NAME_2,
            "enabled": True,
        },
    }
}

CONF_IMPORT_DATA = {CONF_API_KEY: API_KEY, CONF_ACCOUNTS: [ACCOUNT_1, ACCOUNT_2]}


def create_entry(hass: HomeAssistant) -> MockConfigEntry:
    """Add config entry in Home Assistant."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=CONF_DATA,
        options=CONF_OPTIONS,
        unique_id=ACCOUNT_1,
    )
    entry.add_to_hass(hass)
    return entry


class MockedUserInterfaceNull:
    """Mocked user interface returning no players."""

    def GetPlayerSummaries(self, steamids: str) -> dict:
        """Get player summaries."""
        return {"response": {"players": {"player": [None]}}}


class MockedInterface(dict):
    """Mocked interface."""

    def IPlayerService(self) -> None:
        """Mock iplayerservice."""

    def ISteamUser(self) -> None:
        """Mock iSteamUser."""

    def GetFriendList(self, steamid: str) -> dict:
        """Get friend list."""
        return {"friendslist": {"friends": [{"steamid": ACCOUNT_2}]}}

    def GetPlayerSummaries(self, steamids: str) -> dict:
        """Get player summaries."""
        return {
            "response": {
                "players": {
                    "player": [
                        {"steamid": ACCOUNT_1, "personaname": ACCOUNT_NAME_1},
                        {"steamid": ACCOUNT_2, "personaname": ACCOUNT_NAME_2},
                    ]
                }
            }
        }

    def GetOwnedGames(self, steamid: str, include_appinfo: int) -> dict:
        """Get owned games."""
        return {
            "response": {"game_count": 1},
            "games": [{"appid": 1, "img_icon_url": "1234567890"}],
        }

    def GetSteamLevel(self, steamid: str) -> dict:
        """Get steam level."""
        return {"response": {"player_level": 10}}


def patch_interface() -> MockedInterface:
    """Patch interface."""
    return patch("steam.api.interface", return_value=MockedInterface())


def patch_user_interface_null() -> MockedUserInterfaceNull:
    """Patch player interface with no players."""
    return patch("steam.api.interface", return_value=MockedUserInterfaceNull())
