# Cleanup your Kubernates!

## Installation

This python package do not exists in PyPi. Use only with Docker.

## Build

```bash
docker build -t zzzsochi/kubecleaner .
```

## Usage:

```bash
$ docker run -it --rm -v $HOME/.kube/config:/root/.kube/config:ro zzzsochi/kubecleaner --help
 Kubernetes cleaner.

Usage:
  kubecleaner [-n <namespace>] [--dry] jobs <name>

Commands:
  jobs  Delete completed jobs

Global options:
  -h --help     Show this screen.
  -n NAMESPACE  K8S namespace [default: default]
  --dry         Run without deletion
```

```bash
docker run -it --rm -v $HOME/.kube/config:/root/.kube/config:ro zzzsochi/kubecleaner jobs '*'
```

```yaml
---
kind: CronJob
apiVersion: batch/v1beta1
metadata:
  name: cleanup-jobs

spec:
  schedule: "0 */24 * * *"
  successfulJobsHistoryLimit: 1
  failedJobsHistoryLimit: 4
  jobTemplate:
    spec:
      template:
        spec:
          automountServiceAccountToken: true
          restartPolicy: OnFailure
          containers:
          - name: cleaner
            image: zzzsochi/kubecleaner
            command: ["jobs", "drone-job-*"]
```
