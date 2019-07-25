
"""Example of using new architecture for Agent orchestration in PYTEST TESTS."""

from time import sleep


class Test:

    def test_create_agent(self, agent_controller, eapi_device):
        sleep(60)
        agent_controller.send_alert(component_name='clock', instance=1, alert_type='informational_alert', state='set')
        sleep(1)


