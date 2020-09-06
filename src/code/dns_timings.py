import os
import logging.config
import tldextract


log = logging.getLogger('postgres')


def measure_dns(website, har, dns_type, resolver, system):
    domains = get_unique_domains(har)
    domains_filename = "domains.txt"
    write_domains(domains, domains_filename)

    try:
        if dns_type == 'dns':
            dns_type = 'do53'

        elif dns_type == 'doh':
            resolver = convert_resolver(resolver)

        output = system.measure(dns_type, resolver, domains_filename)
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


def convert_resolver(resolver):
    """ Resolver for DoH - convert ip to address """
    if resolver == "1.1.1.1":
        resolver = "cloudflare-dns.com"
    elif resolver == "8.8.8.8":
        resolver = "dns.google"
    elif resolver == "9.9.9.9":
        resolver = "dns.quad9.net"
    return resolver