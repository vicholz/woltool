pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '10', artifactNumToKeepStr: '10'))
        ansiColor('xterm')
        timestamps()
    }
    triggers {
        cron('H/5 * * * *')
    }
    stages {
        stage ('WOLTool - Checkout') {
            steps {
                checkout([$class: 'GitSCM', branches: [[name: '**']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[credentialsId: '', url: 'https://github.com/vicholz/woltool']]])
            }
        }
        stage ('WOLTool - Run') {
            steps {
                withCredentials([
                string(credentialsId: 'WOLTOOL_URL', variable: 'WOLTOOL_URL'),
            ]) {
                    sh '''
set +x

python3 woltool.py \
--debug \
--retries 0 \
--url "${WOLTOOL_URL}"
                    '''
                }
            }
        }
    }
}