import logging
import re

from kubernetes.client import BatchV1Api, CoreV1Api, V1DeleteOptions

logger = logging.getLogger(__name__)


def cleanup_jobs(namespace: str, name: str, dry: bool):
    core = CoreV1Api()
    batch = BatchV1Api()

    job_name_regex = f'^{name.replace("*", ".*")}$'

    for job_name in find_jobs(batch, namespace, job_name_regex):
        logger.info("delete job: %s", job_name)
        if not dry:
            delete_job(batch, namespace, job_name)

        pod_name_regex = f'^{job_name}-.*$'

        for pod_name in find_pods(core, namespace, pod_name_regex):
            logger.info("delete pod: %s", pod_name)
            if not dry:
                delete_pod(core, namespace, pod_name)

def delete_pod(core: CoreV1Api, namespace: str, pod_name: str):
    core.delete_namespaced_pod(pod_name, namespace, V1DeleteOptions())


def delete_job(batch: BatchV1Api, namespace: str, job_name: str):
    batch.delete_namespaced_job(job_name, namespace, V1DeleteOptions())


def find_pods(core: CoreV1Api, namespace: str, name_regex: str):
    for pod in core.list_namespaced_pod(namespace).items:
        if re.match(name_regex, pod.metadata.name):
            yield pod.metadata.name


def find_jobs(batch: BatchV1Api,
              namespace: str, name_regex: str):
    for job in batch.list_namespaced_job(namespace).items:
        if (re.match(name_regex, job.metadata.name) and
                job.status.succeeded == 1):
            yield job.metadata.name
