import os
from fabric.api import env, run, put, cd
from fabric.contrib.files import exists


# Configure hosts


env.hosts = ['stackcite.com']
env.user = os.environ.get('STACKCITE_SSH_USER')
env.key_filename = '~/.ssh/id_rsa.pub'
env.port = 22


# Global constants


_DB_REPO = 'https://github.com/Kobnar/stackcite_db.git'
_API_REPO = 'https://github.com/Kobnar/stackcite_api.git'
_UX_REPO = 'https://github.com/Kobnar/stackcite_ux.git'
_SYS_REPO = 'https://github.com/Kobnar/stackcite_sys.git'
_DEPENDENCIES = ()


# System


def mkdir(path):
    if exists(path) is not True:
        run('mkdir -p {}'.format(path))


def _update_package_index():
    run('sudo apt-get update')


def _upgrade_system():
    run('sudo apt-get -y upgrade')


def update_system():
    _update_package_index()
    _upgrade_system()


def install_deps():
    run('sudo apt-get install -y {}'.format(' '.join(_DEPENDENCIES)))


# Docker


def _install_docker():
    run('sudo apt-get install -y apt-transport-https ca-certificates')
    run('sudo apt-key adv --keyserver hkp://ha.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D')
    run('sudo echo "deb https://apt.dockerproject.org/repo ubuntu-xenial main" | sudo tee /etc/apt/sources.list.d/docker.list')
    _update_package_index()
    run('sudo apt-get install -y linux-image-extra-$(uname -r) linux-image-extra-virtual')
    run('sudo apt-get install -y docker-engine')


def _install_docker_compose():
    run('sudo curl -L "https://github.com/docker/compose/releases/download/1.9.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose')
    run('sudo chmod +x /usr/local/bin/docker-compose')


def _enable_docker_service():
    run('sudo update-rc.d minidlna enable')


def _start_docker_service():
    run('sudo service docker start')


def install_docker():
    _install_docker()
    _install_docker_compose()
    _enable_docker_service()


def start_docker():
    _start_docker_service()


# Container management


def clone_db():
    mkdir('~/src')
    run('git clone -b dev {} ~/src/db'.format(_DB_REPO))


def clone_api():
    mkdir('~/src')
    run('git clone -b dev {} ~/src/api'.format(_API_REPO))


def clone_ux():
    mkdir('~/src')
    run('git clone -b dev {} ~/src/ux'.format(_UX_REPO))


def clone_sys():
    mkdir('~/src')
    run('git clone -b dev {} ~/src/sys'.format(_SYS_REPO))
    run('ln -s ~/src/sys/docker-compose.yml ~/docker-compose.yml')


def clone_all():
    clone_db()
    clone_api()
    clone_ux()
    clone_sys()


def build():
    run('sudo docker-compose build')


def bring_up():
    run('sudo docker-compose up -d')


def bring_down():
    run('sudo docker-compose down')


def clean_all():
    run('rm -Rfv *')
