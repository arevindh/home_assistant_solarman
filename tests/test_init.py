"""Setup, options change and unload against a real HA core (inverter unreachable)."""
from homeassistant.config_entries import ConfigEntryState
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.solarman.const import DOMAIN

OPTIONS = {
    "name": "Inv",
    "inverter_host": "127.0.0.1",
    "inverter_serial": 123,
    "inverter_port": 1,
    "inverter_mb_slaveid": 1,
    "lookup_file": "deye_hybrid.yaml",
}


async def test_setup_options_unload(hass):
    entry = MockConfigEntry(domain=DOMAIN, title="Inv", data=OPTIONS, options=OPTIONS)
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    assert len(hass.states.async_entity_ids("sensor")) > 10
    assert hass.services.has_service(DOMAIN, "write_holding_register")

    hass.config_entries.async_update_entry(entry, options={**OPTIONS, "name": "Renamed"})
    await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.LOADED
    assert entry.title == "Renamed"

    assert await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED
