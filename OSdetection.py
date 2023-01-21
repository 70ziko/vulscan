import subprocess
import platform

def get_installed_software():
    current_os = platform.uname().system.lower()

    if current_os == 'windows':
        command = 'wmic product get name'
    elif current_os == 'darwin':
        command = 'brew list'
    elif current_os == 'linux':
        distro = platform.uname().version
        if 'Ubuntu' or 'Debian' in distro:
            command = 'dpkg-query -l'
        elif 'Fedora' or 'Centos' or 'Redhat' in distro:
            command = 'rpm -qa'
        else:
            command = 'apt list --installed' 
    else:
        return "This script does not support your operating system."

    output = subprocess.check_output(command, shell=True, universal_newlines=True)
    return output

def main():
    print(get_installed_software())
    # print(platform.uname())

if __name__ == "__main__":
    main()