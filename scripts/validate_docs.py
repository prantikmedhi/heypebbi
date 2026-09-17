#!/usr/bin/env python3
"""Validate Pebbi's docs-only pack with Python's standard library.

This is documentation tooling, not application code or a live integration test.
Use the separate OpenAPI/JSON Schema and DESIGN.md linters for full schema/type
and design-spec validation. No network requests or secret reads occur here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []
STATS: Counter = Counter()
SKIP = {'.git', 'node_modules', '__pycache__', '.pebbi-build', 'artifacts'}


def fail(message: str) -> None:
    ERRORS.append(message)


def slug(text: str) -> str:
    text = re.sub(r'<[^>]*>', '', text).strip().lower()
    text = text.replace('`', '')
    text = ''.join(c for c in text if c.isalnum() or c in ' _-')
    return text.replace(' ', '-')


def prose(text: str) -> str:
    return re.sub(r'^(```|~~~).*?^\1[^\n]*$', '', text, flags=re.M | re.S)


def anchors(text: str) -> set[str]:
    out = set(re.findall(r'\b(?:id|name)=[\"\x27]([^\"\x27]+)[\"\x27]', text))
    counts: Counter = Counter()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', prose(text), re.M):
        value = slug(heading)
        index = counts[value]
        counts[value] += 1
        out.add(value + (f'-{index}' if index else ''))
    return out


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in {'href', 'src'} and value:
                self.links.append(value)


def check_link(source: Path, target: str, relative_to_root=False) -> None:
    target = unescape(target).strip().strip('<>')
    if not target or target.startswith(('http:', 'https:', 'mailto:', 'data:', 'tel:', 'urn:')):
        return
    if target.startswith(('javascript:', 'file:')):
        fail(f'{source.relative_to(ROOT)}: unsafe/nonportable link {target}')
        return
    parsed = urlsplit(target)
    if parsed.scheme:
        return
    base = ROOT if relative_to_root else source.parent
    dest = (base / unquote(parsed.path)).resolve() if parsed.path else source
    if not dest.is_relative_to(ROOT):
        fail(f'{source.relative_to(ROOT)}: link escapes repository: {target}')
        return
    if not dest.exists():
        fail(f'{source.relative_to(ROOT)}: broken link {target}')
        return
    if parsed.fragment and dest.is_file() and dest.suffix in {'.md', '.html', '.svg'}:
        if unquote(parsed.fragment) not in anchors(dest.read_text()):
            fail(f'{source.relative_to(ROOT)}: missing anchor {target}')
    STATS['local_links_checked'] += 1


def check_json_refs(path: Path, value, document) -> None:
    if isinstance(value, dict):
        if '$ref' in value:
            ref = value['$ref']
            if ref.startswith('#/'):
                obj = document
                try:
                    for part in ref[2:].split('/'):
                        part = part.replace('~1', '/').replace('~0', '~')
                        obj = obj[int(part)] if isinstance(obj, list) else obj[part]
                    STATS['json_refs_checked'] += 1
                except (KeyError, IndexError, ValueError, TypeError):
                    fail(f'{path.relative_to(ROOT)}: unresolved JSON reference {ref}')
            elif not ref.startswith(('https:', 'urn:')):
                check_link(path, ref.split('#')[0])
        for child in value.values():
            check_json_refs(path, child, document)
    elif isinstance(value, list):
        for child in value:
            check_json_refs(path, child, document)


def frontmatter(path: Path) -> str:
    text = path.read_text()
    match = re.match(r'^---\n(.*?)\n---(?:\n|$)', text, re.S)
    if not match:
        fail(f'{path.relative_to(ROOT)}: missing YAML frontmatter')
        return ''
    return match.group(1)


def validate() -> None:
    manifest = json.loads((ROOT / 'docs/manifest.json').read_text())
    required = manifest['requiredFiles']
    if len(required) != len(set(required)):
        fail('Manifest has duplicate required files')
    for name in required:
        p = ROOT / name
        if not p.is_file() or not p.stat().st_size:
            fail(f'Missing or empty required file: {name}')
    expected = set(manifest['requirementIds'])
    if expected != {f'PB-{i:03d}' for i in range(1, 41)}:
        fail('Manifest must enumerate exactly PB-001 through PB-040')

    paths = [p for p in ROOT.rglob('*') if p.is_file() and not any(x in SKIP for x in p.relative_to(ROOT).parts)]
    for p in paths:
        rel = str(p.relative_to(ROOT))
        if p.suffix in {'.pyc', '.png', '.pdf', '.zip'}:
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            fail(f'Unexpected binary artifact in docs-only pack: {rel}')
            continue
        STATS['text_files_checked'] += 1
        for label, pattern in [
            ('private key', r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
            ('API credential', r'\b(?:sk-[A-Za-z0-9_-]{24,}|gh[pousr]_[A-Za-z0-9]{25,})\b'),
            ('developer home path', r'/Users/[A-Za-z0-9._-]+/'),
            ('unrequested retired brand', r'\b(?:Tavi|Kippi|Mivvi)\b'),
        ]:
            if label == 'unrequested retired brand' and p.suffix == '.py':
                continue  # The checker necessarily contains its own denylist.
            if re.search(pattern, text):
                fail(f'{rel}: found {label}')
        for host in re.findall(r'https://([A-Za-z0-9-]+)\.(?:services\.ai|openai)\.azure\.com', text):
            if host.lower() not in {'example', 'your-resource', 'resource-name', 'your-resource-name'}:
                fail(f'{rel}: concrete private Azure resource host')
        if p.suffix == '.md':
            body = prose(text)
            for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+[\"\x27][^)]*)?\)', body):
                check_link(p, target)
            parser = HTMLLinks()
            parser.feed(body)
            for target in parser.links:
                check_link(p, target)
            if re.search(r'^#{1,6}\s+(?:phase\s*\d|day\s*\d|month\s*\d)', body, re.I | re.M):
                fail(f'{rel}: calendar/staged implementation heading')
        elif p.suffix == '.html':
            parser = HTMLLinks()
            parser.feed(text)
            for target in parser.links:
                check_link(p, target)
            if re.search(r'<script\b|\bonclick\s*=', text, re.I):
                fail(f'{rel}: docs brand board must remain a static reference')
        elif p.suffix == '.svg':
            try:
                svg = ET.fromstring(text)
                tags = [e.tag.rsplit('}', 1)[-1] for e in svg.iter()]
                if 'viewBox' not in svg.attrib or 'title' not in tags or 'desc' not in tags:
                    fail(f'{rel}: SVG lacks accessible title/desc/viewBox')
                if any(t in tags for t in ['script', 'foreignObject', 'image']):
                    fail(f'{rel}: SVG is not self-contained original vector markup')
                for elem in svg.iter():
                    for key, value in elem.attrib.items():
                        if key.rsplit('}', 1)[-1] == 'href' and not value.startswith('#'):
                            fail(f'{rel}: external SVG reference')
                STATS['svg_files_checked'] += 1
            except ET.ParseError as exc:
                fail(f'{rel}: malformed SVG: {exc}')
        elif p.suffix == '.json':
            try:
                doc = json.loads(text)
                check_json_refs(p, doc, doc)
                STATS['json_files_checked'] += 1
            except (ValueError, TypeError) as exc:
                fail(f'{rel}: invalid JSON: {exc}')

    coverage_path = ROOT / 'docs/quality/coverage.json'
    coverage = json.loads(coverage_path.read_text())['requirements']
    ids = [r['id'] for r in coverage]
    if set(ids) != expected or len(ids) != len(expected):
        fail('Coverage must contain every PB ID exactly once')
    for entry in coverage:
        for field in ['requirementDoc', 'flowDoc', 'designDoc', 'acceptanceDoc']:
            check_link(coverage_path, entry[field], relative_to_root=True)
            path = ROOT / entry[field].split('#')[0]
            if path.exists() and entry['id'] not in path.read_text():
                fail(f'{entry["id"]}: absent from {field}')
        if not entry.get('testCases') or not entry.get('verificationClass'):
            fail(f'{entry["id"]}: lacks test cases or verification class')
        for case in entry.get('testCases', []):
            check_link(coverage_path, case, relative_to_root=True)
    for name in ['docs/CONTRACT.md', 'docs/product/REQUIREMENTS.md', 'docs/product/APP-FLOWS.md',
                 'docs/design/SCREENS.md', 'docs/quality/ACCEPTANCE.md']:
        found = set(re.findall(r'PB-\d{3}', (ROOT/name).read_text()))
        if not expected.issubset(found):
            fail(f'{name}: missing requirement IDs {sorted(expected-found)}')
    ledger = json.loads((ROOT/'docs/agents/build-state.template.json').read_text())
    if {r['id'] for r in ledger['requirements']} != expected or ledger['releaseReady'] is not False:
        fail('Build-state template coverage/readiness mismatch')
    if any(r['status'] != 'notStarted' for r in ledger['requirements']):
        fail('Documentation-only build ledger claims implementation progress')

    api = json.loads((ROOT/'docs/engineering/openapi.json').read_text())
    envelope = json.loads((ROOT/'docs/engineering/schemas/tool-envelope.schema.json').read_text())
    if not api['openapi'].startswith('3.1.'):
        fail('API must use OpenAPI 3.1')
    actual_ops = {f'{m.upper()} {path}' for path, value in api['paths'].items() for m in value if m in {'get','post','put','patch','delete'}}
    if actual_ops != set(manifest['restOperations']):
        fail('REST inventory disagrees with manifest')
    if set(api.get('x-websocket', {})) != set(manifest['webSocketPaths']):
        fail('WebSocket inventory disagrees with manifest')
    for key, enum in manifest['stateEnums'].items():
        if api['components']['schemas'][key]['enum'] != enum:
            fail(f'Canonical {key} differs in OpenAPI')
    if api['components']['schemas']['LocalToolName']['enum'] != envelope['$defs']['LocalToolName']['enum']:
        fail('Tool-name enum differs between API and local envelope')
    for data in api.get('x-websocket', {}).values():
        check_link(ROOT/'docs/engineering/openapi.json', data['protocol'])

    skills = {p.parent.name for p in (ROOT/'.claude/skills').glob('*/SKILL.md')}
    for p in (ROOT/'.claude/skills').glob('*/SKILL.md'):
        fm = frontmatter(p)
        if f'name: {p.parent.name}' not in fm or 'description:' not in fm:
            fail(f'{p.relative_to(ROOT)}: invalid skill identity')
    for p in (ROOT/'.claude/agents').glob('*.md'):
        fm = frontmatter(p)
        if f'name: {p.stem}' not in fm or 'model: inherit' not in fm or 'permissionMode: default' not in fm:
            fail(f'{p.relative_to(ROOT)}: agent identity/permission mismatch')
        match = re.search(r'^skills:\n((?:  - [^\n]+\n?)+)', fm, re.M)
        if not match or not set(re.findall(r'  - (\S+)', match.group(1))).issubset(skills):
            fail(f'{p.relative_to(ROOT)}: missing/unknown skill')
    if '@AGENTS.md' not in (ROOT/'CLAUDE.md').read_text():
        fail('CLAUDE.md must import AGENTS.md')
    if 'AGENTS.md' not in (ROOT/'AGENT.md').read_text():
        fail('AGENT.md must redirect to AGENTS.md')
    design_evidence = json.loads((ROOT/'docs/design/verification.json').read_text())
    for artifact in design_evidence.get('files', []):
        asset = ROOT / artifact['path']
        if asset.exists() and hashlib.sha256(asset.read_bytes()).hexdigest() != artifact['sha256']:
            fail(f'{artifact["path"]}: design verification fingerprint is stale')
        STATS['design_fingerprints_checked'] += 1
    STATS['requirements_checked'] = len(expected)
    STATS['rest_operations_checked'] = len(actual_ops)
    STATS['skills_checked'] = len(skills)


def self_test():
    assert slug('Hello **Pebbi**') == 'hello-pebbi'
    assert {'pb-001', 'hello-pebbi'} <= anchors('<a id="pb-001"></a>\n## Hello Pebbi')
    assert 'hidden' not in prose('```text\nhidden\n```\nvisible')
    assert 'visible' in prose('```text\nhidden\n```\nvisible')
    assert anchors('## Same\n## Same') == {'same', 'same-1'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    self_test()
    if args.self_test:
        print('Documentation checker self-tests passed')
        raise SystemExit(0)
    try:
        validate()
    except (OSError, KeyError, ValueError) as exc:
        fail(f'Validation could not complete: {exc}')
    print(json.dumps({'status': 'failed' if ERRORS else 'passed', 'checks': dict(STATS),
                      'errors': ERRORS, 'scope': 'documentation only; no application/live checks'}, indent=2))
    raise SystemExit(1 if ERRORS else 0)
