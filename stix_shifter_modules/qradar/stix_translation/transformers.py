from stix_shifter_utils.stix_translation.src.utils.transformers import ValueTransformer
from stix_shifter_utils.utils import logger

LOGGER = logger.set_logger(__name__)


class QRadarRegistryTransformer(ValueTransformer):
    """A value transformer to convert Registry root key to windows-registry-key STIX"""

    @staticmethod
    def transform(registry):
        LOGGER.debug("QRadarRegistryTransformer", registry)
        stix_root_keys_mapping = {"HKLM": "HKEY_LOCAL_MACHINE", "HKCU": "HKEY_CURRENT_USER",
                                  "HKCR": "HKEY_CLASSES_ROOT", "HKCC": "HKEY_CURRENT_CONFIG",
                                  "HKPD": "HKEY_PERFORMANCE_DATA", "HKU": "HKEY_USERS", "HKDD": "HKEY_DYN_DATA"}
        try:
            splited = registry.split("\\")
            map_root_key = stix_root_keys_mapping[splited[0]]
            splited[0] = map_root_key
            key = '\\'.join(splited)
            return key
        except ValueError:
            LOGGER.error("Cannot convert root key to Stix formatted windows registry key")
