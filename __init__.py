from dualRegevEncryption.Performance import MultiprocEnvSetting


__all__ = [
    "Cipher", 
    "IO",
    "Performance",
]

version_info = (1, 0, '0')

__version__ = ".".join([str(x) for x in version_info])

MultiprocEnvSetting = MultiprocEnvSetting()