import asyncio


WINDOWS_CHECK_VERSION_CMD = ['$PSVersionTable.BuildVersion.Major', '$PSVersionTable.BuildVersion.Minor',
                             '$PSVersionTable.BuildVersion.Build', '$PSVersionTable.BuildVersion.Revision']
LINUX_CHECK_VERSION_CMD = ['lsb_release -i', 'lsb_release -r', 'lsb_release -c']


# add check x64
def check_version(transport_type: int, credential_type: int):
    match (transport_type, credential_type):
        case (0, 0):  # Windows & WinRM
            major, minor, build, revision = (1, 1, 1, 1)  # send cmd
        case (1, 0):  # Linux & SSH
            name, version, code_name = (1, 1, 1)  # send cmd
