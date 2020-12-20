from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class EcsRegistryTransformer(ValueTransformer):
    """A value transformer to convert Registry root key to windows-registry-key STIX"""

    @staticmethod
    def transform(registry):
        LOGGER.debug("EcsRegistryTransformer", registry)
        try:
            reg_key, reg_value = EcsRegistryTransformer.get_reg_key_and_val(registry)
            d = {
                "type": "windows-registry-key",
                "key": reg_key,
                "values": []
            }
            if 'data' in registry:
                for rd in registry['data']['strings']:
                    d['values'].append({
                        "name": reg_value,
                        "data": rd,
                        "data_type": registry['data']['type']
                    })
            return d
        except ValueError:
            LOGGER.error("Cannot convert root key to STIX formatted windows registry key")

    @staticmethod
    def get_reg_key_and_val(registry):
        stix_root_keys_mapping = {"HKLM": "HKEY_LOCAL_MACHINE", "HKCU": "HKEY_CURRENT_USER",
                                  "HKCR": "HKEY_CLASSES_ROOT", "HKCC": "HKEY_CURRENT_CONFIG",
                                  "HKPD": "HKEY_PERFORMANCE_DATA", "HKU": "HKEY_USERS", "HKDD": "HKEY_DYN_DATA"}

        reg_key = registry['path'].split("\\")
        map_root_key = stix_root_keys_mapping[reg_key[0]]
        reg_key[0] = map_root_key
        reg_value = reg_key[-1]
        reg_key = reg_key[:-1]
        key = '\\'.join(reg_key)
        return key, reg_value
