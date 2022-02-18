import os
from textwrap import dedent

from .cluster_manager import ClusterManager


class PyenvClusterManager(ClusterManager):
    BOOTSTRAP = dedent("""\
        #!/bin/bash

        set -e
        ENV_NAME={project_name}-env
        VERS=$(pyenv versions)
        if [[ ! $VERS =~ (^|[[:space:]])$ENV_NAME($|[[:space:]]) ]]
        then            
            pyenv install {python_version} -s
            pyenv virtualenv {python_version} $ENV_NAME
        fi
        pyenv local {project_name}-env
        
        pip install automan

        # Run any requirements.txt from the user
        cd ..
        if [ -f "requirements.txt" ] ; then
            pip install -r requirements.txt
        fi
        """)

    UPDATE = dedent("""\
         #!/bin/bash

         set -e
         pyenv local {project_name}-env
         # Run any requirements.txt from the user
         cd {project_name}
         if [ -f "requirements.txt" ] ; then
             pip install -r requirements.txt
         fi
         """)

    def _get_bootstrap_code(self):
        import platform
        return self.BOOTSTRAP.format(project_name=self.project_name,
                                     python_version=platform.python_version())

    def _get_python(self, host, home):
        return 'python'

    def _get_helper_scripts(self):
        return None

    def _get_update_code(self):
        return self.UPDATE.format(project_name=self.project_name)
