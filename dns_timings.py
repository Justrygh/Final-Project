import sys
import os
import subprocess
import uuid
import logging.config
import collections
import subprocess
import tldextract
from subprocess import call, run, PIPE, check_output, STDOUT
import platform
import wslpy as wp

log = logging.getLogger('postgres')


def measure_dns(website, har, dns_type, resolver):
    operation_system = platform.system()
    domains = get_unique_domains(har)
    domains_filename = "domains.txt"
    write_domains(domains, domains_filename)

    try:
        if dns_type == 'dns':
            dns_type = 'do53'

        if operation_system == "Linux":
            cmd = ["dns-timing/dns-timing", dns_type, resolver, domains_filename]
            output = check_output(cmd, stderr=STDOUT)

        elif operation_system == "Windows":
            cmd = "dns-timing/dns-timing {0} {1} {2}".format(dns_type, resolver, domains_filename)
            project_path = os.getcwd()
            project_path = project_path.split("\\")
            project_path[0] = project_path[0][:-1].lower()
            project_path = "/".join(project_path)
            project_path = "cd ../../mnt/" + project_path
            run_input = project_path + " && " + cmd
            output = run("ubuntu", shell=True, stdout=PIPE, input=run_input, encoding='ascii')

        output = output.decode('utf-8')
        all_dns_info = parse_output(output, website, domains)
        os.remove(domains_filename)
        return all_dns_info
    except Exception as e:
        err = 'Error getting DNS timings: website {0}, dns_type {1}, ' \
              'resolver {2}'
        os.remove(domains_filename)
        log.error(err.format(website, dns_type, resolver))
    return None


def parse_output(output, website, domains):
    # Initialize the dict with all domains in the HAR
    all_dns_info = {}
    for domain in domains:
        all_dns_info[domain] = {'response_time': 0.,
                                'response_size': 0,
                                'error': 0}

    # If there's no output from the DNS tool, return immediately
    if not output:
        return all_dns_info

    # For each domain in the HAR, record DNS response time and size
    try:
        lines = output.splitlines()
        for line in lines:
            status, domain, response_time, size_or_error = line.split(',', 4)
            if status == "ok":
                response_size = int(size_or_error)
                error = None
            else:
                response_size = None
                error = int(size_or_error)

            all_dns_info[domain] = {'response_time': float(response_time),
                                    'response_size': response_size,
                                    'error': error}
    except Exception as e:
        err = 'Error parsing DNS output for website {0}: {1}'
        log.error(err.format(website, e))
    return all_dns_info


def get_unique_domains(har):
    if not har:
        return []

    log = har["log"]
    if "entries" not in log:
        return []
    entries = log["entries"]

    if len(entries) == 1:
        return []

    domains = []
    for entry in entries:
        # If a DNS request was made, record the timings
        if "request" not in entry:
            continue
        request = entry["request"]

        if "url" not in request:
            continue
        url = request["url"]

        ext = tldextract.extract(url)
        if ext.subdomain:
            fqdn = ext.subdomain + "." + ext.domain + "." + ext.suffix
        else:
            fqdn = ext.domain + "." + ext.suffix
        domains.append(fqdn)
    return list(set(domains))


def write_domains(domains, domains_filename):
    with open(domains_filename, 'w') as f:
        for d in domains:
            f.write("{0}\n".format(d))
        f.close()
