"""Convert public upstream text data to Shadowrocket RULE-SET files.

Only sources.json is read. No user YAML, credentials, or proxy configuration
is needed, and downloaded content is treated as data, never executable code.
"""
import concurrent.futures
import hashlib
import ipaddress
import json
from pathlib import Path
import urllib.request

ROOT = Path(__file__).resolve().parent


def convert(source, content):
    rows = []
    for entry in content.decode('utf-8-sig').splitlines():
        entry = entry.strip()
        if not entry or entry.startswith('#'):
            continue
        if source['behavior'] == 'domain':
            if entry.startswith('+.'):
                row = 'DOMAIN-SUFFIX,' + entry[2:]
            elif entry.startswith('.'):
                row = 'DOMAIN-WILDCARD,*' + entry
            else:
                if any(c in entry for c in '*,:/ '):
                    raise ValueError('Unsupported domain entry in ' + source['name'])
                row = 'DOMAIN,' + entry
        elif source['behavior'] == 'ipcidr':
            net = ipaddress.ip_network(entry, strict=False)
            row = ('IP-CIDR6,' if net.version == 6 else 'IP-CIDR,') + entry
        else:
            fields = entry.split(',')
            if fields[0] not in {'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'IP-CIDR', 'IP-CIDR6'}:
                raise ValueError('Unsupported classical entry in ' + source['name'])
            if len(fields) != 2 and not (len(fields) == 3 and fields[2] == 'no-resolve'):
                raise ValueError('Unexpected policy or flag in public source')
            row = entry
        rows.append(row)
    if not rows:
        raise ValueError('Empty rule source: ' + source['name'])
    header = '# Public upstream data converted for Shadowrocket\n# Source: ' + source['url'] + '\n'
    return (header + '\n'.join(rows) + '\n').encode(), len(rows)


def fetch(source):
    request = urllib.request.Request(source['url'], headers={'User-Agent': 'ShadowrocketRuleConverter/1.0'})
    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read(20_000_001)
    if len(content) > 20_000_000:
        raise ValueError('Rule source exceeds size limit')
    result, count = convert(source, content)
    return source, content, result, count


def main():
    sources = json.loads((ROOT / 'sources.json').read_text())
    # Collect and validate every response before replacing any existing file.
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch, sources))
    directory = ROOT / 'rules'
    directory.mkdir(exist_ok=True)
    manifest = []
    for source, content, result, count in results:
        (directory / (source['name'] + '.list')).write_bytes(result)
        manifest.append({'name': source['name'], 'url': source['url'], 'rules': count,
                         'source_sha256': hashlib.sha256(content).hexdigest(),
                         'converted_sha256': hashlib.sha256(result).hexdigest()})
    (ROOT / 'rules-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Validated and converted %d public rule sets.' % len(results))


if __name__ == '__main__':
    main()
