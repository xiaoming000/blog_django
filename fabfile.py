from fabric.api import env, run
from fabric.operations import sudo

GIT_REPO = "git@github.com:xiaoming000/blog_django.git" 

env.user = 'xiao'
env.password = '950909'

env.hosts = ['www.dmfly.xin']

env.port = '22'


def deploy():
    source_folder = '/home/xiao/sites/www.dmfly.xin/blog_django'

    run('cd %s && git pull' % source_folder) 
    run("""
        cd {} &&
        ../env/bin/pip install -r requirements.txt &&
        ../env/bin/python3 manage.py collectstatic --noinput &&
        ../env/bin/python3 manage.py migrate
        """.format(source_folder))
    sudo('systemctl restart www.dmfly.xin.service') 
    sudo('service nginx reload')
