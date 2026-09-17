#!/usr/bin/env python3
"""Static schema regression checks for reviewed Pebbi contracts.

Requires jsonschema. These synthetic fixtures never call providers, authenticate
real users, write a product file, execute generated code or claim runtime safety.
"""
import copy
import json
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
api = json.loads((ROOT / 'docs/engineering/openapi.json').read_text())
local = json.loads((ROOT / 'docs/engineering/schemas/tool-envelope.schema.json').read_text())
checks = []
UUID = '00000000-0000-4000-8000-000000000001'


def api_validator(name):
    return Draft202012Validator({'$ref': '#/components/schemas/' + name,
                                 'components': api['components']}, format_checker=FormatChecker())


def local_validator(name):
    return Draft202012Validator({'$ref': '#/$defs/' + name, '$defs': local['$defs']},
                               format_checker=FormatChecker())


def expect(validator, value, valid, label):
    errors = list(validator.iter_errors(value))
    assert (not errors) == valid, label + ': ' + '; '.join(e.message for e in errors[:3])
    checks.append(label)


# Device ID alone cannot meet the declared device-bound API contract.
exempt = {'GET /healthz', 'GET /v1/me', 'POST /v1/devices', 'POST /v1/devices/enrollments',
          'POST /v1/billing/webhook', 'POST /v1/usage/reservations/{reservationId}/finalize'}
for path, methods in api['paths'].items():
    for method, spec in methods.items():
        if method not in {'get', 'post', 'put', 'patch', 'delete'}:
            continue
        op = method.upper() + ' ' + path
        if op in exempt:
            continue
        refs = {p.get('$ref') for p in spec.get('parameters', [])}
        assert '#/components/parameters/DeviceId' in refs, op
        assert '#/components/parameters/DeviceToken' in refs, op
checks.append('every device-bound REST operation declares both identity and credential headers')
assert '/v1/devices/enrollments' in api['paths']
enrollment = api['paths']['/v1/devices/enrollments']['post']
challenge_ref = enrollment['responses']['201']['content']['application/json']['schema']['$ref']
challenge_schema = api['components']['schemas'][challenge_ref.rsplit('/', 1)[-1]]
assert {'enrollmentId', 'authorizationNonce', 'expiresAt'} <= set(challenge_schema['required'])
checks.append('enrollment uses an explicit standard-OIDC nonce challenge')
registration = api['components']['schemas']['RegisterDeviceRequest']
assert {'enrollmentId', 'enrollmentIdToken'} <= set(registration['required'])
assert 'enrollmentAssertion' not in registration['properties']
checks.append('registration requires nonce-bound ID-token proof, not an invented assertion issuer')
assert 'deviceToken' in api['components']['schemas']['RegisterDeviceResponse']['required']
expect(api_validator('DeviceToken'), 'A' * 43, True, 'synthetic device-token format accepted')
expect(api_validator('DeviceToken'), UUID, False, 'public UUID cannot masquerade as device credential')
expect(api_validator('DeviceToken'), 'A' * 42, False, 'short device credential rejected')

# A model cannot invent an artifact UUID before an explicit content-producing call.
assert api['components']['schemas']['LocalToolName']['enum'] == local['$defs']['LocalToolName']['enum']
assert 'stageTextArtifact' in local['$defs']['LocalToolName']['enum']
args = {'workspaceId': UUID, 'draftId': None, 'chunkIndex': 0,
        'text': 'A Pebbi-authored document. 漢字', 'mimeType': 'text/plain', 'final': True}
expect(local_validator('StageTextArtifactArguments'), args, True, 'first authored UTF-8 chunk accepted')
bad = dict(args, chunkIndex=1)
expect(local_validator('StageTextArtifactArguments'), bad, False, 'new draft cannot skip first chunk')
bad = dict(args, approvalGranted=True)
expect(local_validator('StageTextArtifactArguments'), bad, False, 'artifact arguments cannot carry invented authority')
bad = dict(args, mimeType='application/octet-stream')
expect(local_validator('StageTextArtifactArguments'), bad, False, 'arbitrary binary staging rejected')
expect(local_validator('StageTextArtifactOutput'), {'draftId': UUID, 'nextChunkIndex': 1},
       True, 'unfinished draft has no fabricated final artifact')
final = {'draftId': UUID, 'nextChunkIndex': 1, 'artifactId': UUID,
         'byteCount': 0, 'sha256': '0' * 64, 'mimeType': 'text/plain'}
# Zero digest is a formatting fixture, not a claim about any actual file hash.
expect(local_validator('StageTextArtifactOutput'), final, True, 'final artifact output has immutable digest fields')
bad = dict(final)
del bad['sha256']
expect(local_validator('StageTextArtifactOutput'), bad, False, 'incomplete final artifact metadata rejected')
code = {'workspaceId': UUID, 'scriptArtifactId': UUID, 'expectedSha256': '0' * 64,
        'inputFileVersionIds': [], 'arguments': [], 'timeoutSeconds': 1}
expect(local_validator('RunCodeArguments'), code, True, 'script uses immutable artifact and expected digest')
expect(local_validator('RunCodeArguments'), dict(code, scriptVersionId=UUID), False,
       'undefined scriptVersionId cannot reappear')

# Unknown context capacity cannot be hidden behind a ready reasoning capability.
cap = {'role': 'reasoning', 'model': 'gpt-6-astra', 'state': 'failed', 'reason': 'Synthetic test',
       'supportsScreenInput': False, 'supportsTools': False, 'audioFormats': [], 'voices': [],
       'verifiedAt': None, 'supportsContextInput': False, 'tokenBudget': None}
expect(api_validator('RoleCapability'), cap, True, 'unavailable budget is represented honestly')
expect(api_validator('RoleCapability'), dict(cap, state='ready'), False,
       'reasoning ready without verified budget rejected')
expect(api_validator('RoleCapability'), dict(cap, model='gpt-realtime-2.1'), False,
       'wrong locked model for reasoning rejected')

# JSON character counts are not encoded message-byte limits.
message = {'schemaVersion': 1, 'payload': {'text': '漢' * 11000}}
serialized = json.dumps(message, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
assert 32 * 1024 < len(serialized) <= 256 * 1024
escaped = json.dumps({'payload': {'text': '😀' * 32000}}, ensure_ascii=True).encode('utf-8')
assert len(escaped) > 256 * 1024
checks.append('multibyte text needs control-message budget larger than audio-message budget')
checks.append('escape-heavy valid text still requires serialized-byte enforcement')

print(json.dumps({'status': 'passed', 'checks': checks, 'checkCount': len(checks),
                  'scope': 'synthetic static schema/budget checks only; not native/live/security execution'}, indent=2))
