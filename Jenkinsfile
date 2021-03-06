node('master'){
  withEnv(['PATH=/apps/download/n/8/bin:/s00/bin:/apps/sonarscanner/bin:/bin:/usr/bin:/s00/libexec/git-core', 'LD_LIBRARY_PATH=/apps/download/n/8/lib:/s00/lib64:/apps/sonarscanner/lib:/lib64:/usr/lib64']) {

  stage('SonarScan') {
    deleteDir()
	git branch: '${gitTag}', url: 'https://github.com/bcgov/kirk'
    tool name: 'sonarscanner'
    withSonarQubeEnv('CODEQA') {
    dir('.') {
    sh '''
       sonar-scanner -Dsonar.sources="." -Dsonar.exclusions="node_modules/**/*" -Dsonar.projectKey="kirk" -Dsonar.projectVersion="${gitTag}" -Dsonar.login="${sonarToken}"
       '''
    def props = readProperties  file: '.scannerwork/report-task.txt'
    echo "properties=${props}"
    env.sonarServerUrl=props['serverUrl']
    env.SONAR_CE_TASK_URL=props['ceTaskUrl']
    def ceTask
        timeout(time: 1, unit: 'MINUTES') {
          waitUntil {
            sh 'curl -u $sonarToken $SONAR_CE_TASK_URL -o ceTask.json'
            ceTask = readJSON file: 'ceTask.json'
            echo ceTask.toString()
            return "SUCCESS".equals(ceTask["task"]["status"])
          }
        }
        env.qualityGateUrl = env.sonarServerUrl + "/api/qualitygates/project_status?analysisId=" + ceTask["task"]["analysisId"]
        sh 'curl -u $sonarToken $qualityGateUrl -o qualityGate.json'
        def qualitygate = readJSON file: 'qualityGate.json'
        echo qualitygate.toString()
        if ("ERROR".equals(qualitygate["projectStatus"]["status"])) {
          error  "Quality Gate failure"
        }
        echo  "Quality Gate success"
      }
     }
    }

  stage ('OCP build'){
    sh '''echo "It will take 2 minutes for OpenShift rolling new install to runtime"'''
    def response = httpRequest contentType: 'APPLICATION_JSON_UTF8', httpMode: 'POST', requestBody: "{}", url: "${ocpBH}"
    ocpTask = readJSON text: response.content
    echo ocpTask.toString()
    return "Success".equals(ocpTask["status"])
  }
 }
}
