""" Tests the creation and loading of a platform via the API """

from typing import cast
from unittest.mock import MagicMock, patch

from qiboconnection.api import API
from qiboconnection.connection import Connection

from ..data import (
    sample_all_platform_settings,
    sample_bus_model_data,
    sample_component_model_data,
    sample_platform_settings_model_data,
    sample_schema_model_data,
)


class TestAPIPlatform:
    """Tests the creation and loading of a platform via the API"""

    def test_build_a_complete_platform(self, mocked_api: API):
        """build a complete platform"""

        # create a platform settings
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 1} | sample_platform_settings_model_data, 201),
        ):
            platform_settings = mocked_api.create_platform_settings(
                platform_settings=sample_platform_settings_model_data
            )
        platform_settings_id = cast(int, platform_settings.get("id_"))

        # create a platform schema settings
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 1} | sample_schema_model_data, 201),
        ):
            platform_schema_settings = mocked_api.create_platform_schema_settings(
                platform_settings_id=platform_settings_id, platform_schema_settings=sample_platform_settings_model_data
            )
        platform_schema_settings_id = cast(int, platform_schema_settings.get("id_"))
        assert platform_schema_settings_id == 1

        # create a platform bus settings
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 1} | sample_bus_model_data, 201),
        ):
            platform_first_bus_settings = mocked_api.create_platform_bus_settings(
                platform_schema_settings_id=platform_schema_settings_id, platform_bus_settings=sample_bus_model_data
            )
        platform_first_bus_settings_id = cast(int, platform_first_bus_settings.get("id_"))
        assert platform_first_bus_settings_id == 1

        # create a platform component (qblox_qcm) to a specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 1} | sample_component_model_data, 201),
        ):
            qblox_qcm_settings_first_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_first_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qcm_settings_first_bus_id = cast(int, qblox_qcm_settings_first_bus.get("id_"))
        assert qblox_qcm_settings_first_bus_id == 1

        # create another platform component (rohde_schwarz) to a specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 2} | sample_component_model_data, 201),
        ):
            qblox_rohde_schwarz_settings_first_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_first_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_rohde_schwarz_settings_first_bus = cast(int, qblox_rohde_schwarz_settings_first_bus.get("id_"))
        assert qblox_rohde_schwarz_settings_first_bus == 2

        # create another platform component (mixer) to a specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 3} | sample_component_model_data, 201),
        ):
            qblox_mixer_settings_first_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_first_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_mixer_settings_first_bus = cast(int, qblox_mixer_settings_first_bus.get("id_"))
        assert qblox_mixer_settings_first_bus == 3

        # create another platform component (resonator) to a specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 4} | sample_component_model_data, 201),
        ):
            qblox_resonator_settings_first_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_first_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_resonator_settings_first_bus_id = cast(int, qblox_resonator_settings_first_bus.get("id_"))
        assert qblox_resonator_settings_first_bus_id == 4

        # create another platform component (qubit) to a specific component
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 5} | sample_component_model_data, 201),
        ):
            qblox_qubit_settings_first_bus = mocked_api.create_platform_component_settings(
                platform_component_parent_settings_id=qblox_resonator_settings_first_bus_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qubit_settings_first_bus = cast(int, qblox_qubit_settings_first_bus.get("id_"))
        assert qblox_qubit_settings_first_bus == 5

        # create another platform bus settings
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 2} | sample_bus_model_data, 201),
        ):
            platform_second_bus_settings = mocked_api.create_platform_bus_settings(
                platform_schema_settings_id=platform_schema_settings_id, platform_bus_settings=sample_bus_model_data
            )
        platform_second_bus_settings_id = cast(int, platform_second_bus_settings.get("id_"))
        assert platform_second_bus_settings_id == 2

        # create a platform component (qblox_qrm) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 6} | sample_component_model_data, 201),
        ):
            qblox_qrm_settings_second_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_second_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qrm_settings_second_bus = cast(int, qblox_qrm_settings_second_bus.get("id_"))
        assert qblox_qrm_settings_second_bus == 6

        # create another platform component (rohde_schwarz) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 7} | sample_component_model_data, 201),
        ):
            qblox_rohde_schwarz_settings_second_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_second_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_rohde_schwarz_settings_second_bus = cast(int, qblox_rohde_schwarz_settings_second_bus.get("id_"))
        assert qblox_rohde_schwarz_settings_second_bus == 7

        # create another platform component (resonator) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 8} | sample_component_model_data, 201),
        ):
            qblox_resonator_settings_second_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_second_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_resonator_settings_second_bus = cast(int, qblox_resonator_settings_second_bus.get("id_"))
        assert qblox_resonator_settings_second_bus == 8

        # create another platform component (qubit) to another specific component
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 9} | sample_component_model_data, 201),
        ):
            qblox_qubit_settings_second_bus = mocked_api.create_platform_component_settings(
                platform_component_parent_settings_id=qblox_resonator_settings_second_bus,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qubit_settings_second_bus = cast(int, qblox_qubit_settings_second_bus.get("id_"))
        assert qblox_qubit_settings_second_bus == 9

        # create another platform component (mixer) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 10} | sample_component_model_data, 201),
        ):
            qblox_mixer_settings_second_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_second_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_mixer_settings_second_bus = cast(int, qblox_mixer_settings_second_bus.get("id_"))
        assert qblox_mixer_settings_second_bus == 10

        # create another platform bus settings
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 3} | sample_bus_model_data, 201),
        ):
            platform_third_bus_settings = mocked_api.create_platform_bus_settings(
                platform_schema_settings_id=platform_schema_settings_id, platform_bus_settings=sample_bus_model_data
            )
        platform_third_bus_settings_id = cast(int, platform_third_bus_settings.get("id_"))
        assert platform_third_bus_settings_id == 3

        # create a platform component (qblox_qrm) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 11} | sample_component_model_data, 201),
        ):
            qblox_qblox_qrm_settings_third_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_third_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qblox_qrm_settings_third_bus = cast(int, qblox_qblox_qrm_settings_third_bus.get("id_"))
        assert qblox_qblox_qrm_settings_third_bus == 11

        # create another platform component (rohde_schwarz) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 12} | sample_component_model_data, 201),
        ):
            qblox_qblox_rohde_schwarz_settings_third_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_third_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qblox_rohde_schwarz_settings_third_bus = cast(
            int, qblox_qblox_rohde_schwarz_settings_third_bus.get("id_")
        )
        assert qblox_qblox_rohde_schwarz_settings_third_bus == 12

        # create another platform component (resonator) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 13} | sample_component_model_data, 201),
        ):
            qblox_qblox_resonator_settings_third_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_third_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qblox_resonator_settings_third_bus = cast(int, qblox_qblox_resonator_settings_third_bus.get("id_"))
        assert qblox_qblox_resonator_settings_third_bus == 13

        # create another platform component (qubit) to another specific component
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 14} | sample_component_model_data, 201),
        ):
            qblox_qblox_qubit_settings_third_bus = mocked_api.create_platform_component_settings(
                platform_component_parent_settings_id=qblox_qblox_resonator_settings_third_bus,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qblox_qubit_settings_third_bus = cast(int, qblox_qblox_qubit_settings_third_bus.get("id_"))
        assert qblox_qblox_qubit_settings_third_bus == 14

        # create another platform component (mixer) to another specific bus
        with patch.object(
            Connection,
            "send_post_auth_remote_api_call",
            return_value=({"id_": 15} | sample_component_model_data, 201),
        ):
            qblox_qblox_mixer_settings_third_bus = mocked_api.create_platform_component_settings(
                platform_bus_settings_id=platform_third_bus_settings_id,
                platform_component_settings=sample_component_model_data,
            )
        qblox_qblox_mixer_settings_third_bus = cast(int, qblox_qblox_mixer_settings_third_bus.get("id_"))
        assert qblox_qblox_mixer_settings_third_bus == 15

    @patch.object(
        Connection,
        "send_get_auth_remote_api_call",
        return_value=(sample_all_platform_settings, 200),
    )
    def test_load_all_platform_settings(self, patched_connection: MagicMock, mocked_api: API):
        """load all platform settings"""
        response = mocked_api.load_all_platform_settings(
            platform_settings_id=cast(int, sample_all_platform_settings["platform"]["id_"])
        )
        assert isinstance(response, dict)
        assert response == sample_all_platform_settings
        patched_connection.assert_called_once()
