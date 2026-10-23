## Verity: System Process and Architecture Blueprint (India + EU)

Team CodeVerse · Prepared 20 October 2026

What this is: the full working design of KYCVault for India and the EU: what the system does, how each flow runs once it is live, the complete architecture, and a step-by-step plan to move from the current code (the idbi repository) to the target system.

How to read it: each component is tagged [Keep] (works today, stays), [Change] (exists, must be modified), or [New] (does not exist yet). Items marked verify depend on legal or vendor facts that must be confirmed before launch. This is a technical design, not legal advice.

## Design decisions this blueprint assumes

These were chosen to fit both Indian KYC rules and GDPR. If any is changed, the affected sections will need updating.

| # Decision Why D1 Two independent regional cells: India Data residency, DPDP and GDPR transfer (Mumbai) and EU (Frankfurt). No shared rules. database. D2 KYCVault is a technology provider / Receiving banks stay legally responsible processor for regulated banks' KYC for KYC. records, and a controller / fiduciary only for the person's own credential layer. D3 Storage is split into two layers: an Erasure rights collide with PMLA and erasable credential and consent layer, AMLR retention. and a retention-locked regulatory |
| --- |
| record. D4 The chain (if kept) holds only a daily EDPB final blockchain guidelines. Merkle root. No per-person hash. Revocation uses off-chain status lists. |


| # | Decision | Why |
| --- | --- | --- |
| D5 Credentials are issued in a dual profile: |   | EU wallets use specific formats and |
|   | an EUDI-compatible one with a | algorithms. |
|   | conventional signature, and an ML-DSA- |   |
|   | 87 post-quantum one. |   |
| D6 | No Aadhaar number, XML or biometrics | Aadhaar Act restrictions. |
|   | are stored. Only derived attributes. |   |
| D7 Cloud follows the Master Plan: AWS. The |   | One cloud, per-region KMS, PQC |
|   | current GCP design is reused as a | support. |
|   | pattern. |   |

## 1. What the system does

KYCVault holds a person's verified identity as separately encrypted facts, issues a signed credential from those facts, and answers a verifier's question with the smallest true answer. It supports two ways of answering:

- Proof mode for businesses that only need a fact (hotel, platform, telecom): "over 18: yes" or "name matches".

- Reliance mode for regulated entities that must obtain CDD records when relying on another institution's KYC: a consented release of the verified KYC file plus a signed trail.

What it is not: a replacement for CKYCR, V-CIP, DigiLocker, Aadhaar or the EUDI Wallet. It sits between those rails and the businesses that ask for ID.

## 2. Starting point: the current system

| Area | Today | Action |
| --- | --- | --- |
| Chain contract | Operator-only writes. Stores | [Change] Stop storing per- |
| KYCVault.sol | SHA-256 of the PII payload, | person hashes. Replace |
|   | consent bits, verifier | with a root-anchor |
|   | address. | contract. |


| Area | Today | Action |
| --- | --- | --- |
| Backend (Express, | 15 routes, JWT, role guards, | [Change] Split into |
| TypeScript) | rate limits, 60-second self- | services. Remove self- |
|   | destruct sweep. | destruct for regulated |
|   |   | records. |
| Encryption | Per-record DEK wrapped by | [Change] One encrypted |
|   | Cloud KMS KEK (AAD = | fact per row. Keep envelope |
|   | publicId), one blob per | pattern. |
|   | customer. |   |
| Operator-relayer model | Users hold no wallet or keys. | [Change] Add a user-held |
|   |   | holder key (passkey). Keep |
|   |   | relayer only if chain stays. |
| Database | 5 tables on Cloud SQL. Old | [Change] New 11+ table |
|   | data is lost; structure | schema (section 4). |
|   | recovered. |   |
| Consent | Per-partner boolean in DB | [Change] Rich consent |
|   | and on chain. | object with purpose, basis |
|   |   | and expiry. |
| OTP sharing | 6-digit, 5 min, scoped | [Keep] Reuse as in-person |
|   | disclosure. | presentation channel. |
| Age-only and proof-of- | Server-side redaction. | [Change] Replace with |
| existence |   | signed selective disclosure. |
| Access log | Pseudonymous, survives | [Keep] Add region and |
|   | erasure. | retention fields. |
| OCR (Vision API) | Primary data entry path. | [Change] Fallback only. |
|   |   | Primary data comes from |
|   |   | issuer rails. |
| Terraform, KMS runbook, | GCP. | [Change] Port to AWS |
| CMEK, Secret Manager |   | equivalents. |
| patterns |   |   |
| Frontends (React) | Verifier, customer, partner | [Change] Rename to Issuer |
|   | screens. | console, Person vault, |
|   |   | Verifier console. |
| viz/ timing animation | Stage tool. | [Keep] Optional. |


## 3. Target architecture

## 3.1 Overview

```
PERSON (phone / browser) VERIFIER (bank, hotel, platform)
Vault app + holder key (passkey) Verifier console + SDK
| |
| TLS (hybrid ML-KEM) |
v v
+--------------------- REGION ROUTER (no PII) ----------------------+
| chooses cell by: user choice > issuer > device > IP |
+-----------------------------+------------------------------------+
|
+-----------------------+------------------------+
| |
INDIA CELL (ap-south-1) EU CELL (eu-central-1)
---------------------------------------------------------------------
API gateway + auth (OIDC, passkeys, rate limits)
Issuer adapters : DigiLocker, Aadhaar offline XML, bank (CKYCR) | EUDI
PID import, eID, bank
Credential service: SD-JWT VC, dual profile, status lists
Consent service : purpose, basis, scope, expiry, revocation
Policy engine : per-region rules file, verifier registry
Retention engine : legal hold, schedules, erasure queue
Audit service : pseudonymous access log, presentation log
Key service : KMS (AES-256 wrap, ML-DSA-87, ES256)
Data tier : Postgres (encrypted facts, metadata), object store (V-
CIP/evidence if hosted)
Notification : consent requests, expiry, update-due
---------------------------------------------------------------------
| |
+----------- daily Merkle root only ------------+
|
Anchor service (optional chain)
```

## 3.2 Regional cells

- Each cell is a full deployment: its own database, KMS keys, secrets, logs and rules file. Code is identical; configuration differs.


- India cell: Mumbai region. Holds data of people issued identity in India. Logs kept in India for a rolling 180 days (CERT-In). Payment-related data stays in India.

- EU cell: Frankfurt region. Holds data of EU residents and EUDI-sourced credentials. Transfers out of the EU only under a transfer mechanism.

- Region router: a stateless service holding no personal data. Signals in priority order: the person's saved choice, the issuing rail (an Aadhaar-verified person belongs to India), device region, IP.

- No global person index (change from the Master Plan). A random ID tied to a region is still personal data under GDPR. Route by issuer and a per-cell lookup instead. If a global index is kept, treat it as personal data.

- Travel changes nothing. Relocation is a consented migration (roadmap).

## 3.3 Services

| Service | Job | Status |
| --- | --- | --- |
| API gateway and | OIDC login, passkey enrolment, role guards | [Change] |
| auth | (PERSON, ISSUER, VERIFIER, COMPLIANCE, |   |
|   | ADMIN), rate limits |   |
| Issuer adapters | Turn a rail's output into attribute facts: DigiLocker | [New] |
|   | (sandbox first), Aadhaar offline XML (verify |   |
|   | signature offline), bank-issued KYC, EUDI PID |   |
|   | import, national eID |   |
| Credential service | Build SD-JWT VC, sign (dual profile), manage | [New] |
|   | status lists, set expiry and next-update-due |   |
| Consent service | Create, track, revoke consents with purpose, | [Change] |
|   | recipient, lawful basis, scope, expiry |   |
| Presentation service Check a verifier's request against its registered |   | [New] |
|   | scope, run consent, return a proof or reliance |   |
|   | package |   |
| Policy engine | Per-region and per-verifier-class rules: which | [New] |
|   | facts may ever be asked |   |
| Retention engine | Compute retention per record; legal holds; | [New] |
|   | erasure queue; automatic deletion at expiry |   |


| Service | Job | Status |
| --- | --- | --- |
| Audit service | Pseudonymous access and presentation logs, | [Keep/Change] |
|   | exportable evidence |   |
| Key service | KMS wrappers for DEKs, signing, rotation, | [Change] |
|   | key_epoch |   |
| Anchor service | Daily Merkle root of credential and consent | [New, optional] |
|   | hashes, signed hash-based, written on chain |   |
| Notification | Consent requests, expiry and update-due | [New] |
|   | reminders, withdrawal notices to verifiers |   |
| Compliance console Retention schedules, legal holds, DPIA artefacts, |   | [New] |
|   | regulator export, grievance queue |   |

## 3.4 Data model

Eleven tables from the Master Plan, with changes for India and EU compliance, and three added.

| Table | Holds | Key points |
| --- | --- | --- |
| subject | Random public ID, home cell, | No personal data. |
|   | status, created date |   |
| attribute | One encrypted fact per row: | Per-fact encryption and |
|   | type, ciphertext, wrapped DEK, | erasure. |
|   | key_epoch id, salted keyed hash |   |
| credential | Issued SD-JWT: issuer, type, | Supports India's 2/8/10-year |
|   | profile (EUDI/PQ), signature alg, | updation and EU's yearly/5- |
|   | issue and expiry date, assurance | year cycle. |
|   | level, cdd_level, |   |
|   | next_update_due, status-list |   |
|   | index |   |
| disclosure_policy | Per region and verifier class: | The rules file as data. |
|   | allowed attributes |   |


| Table | Holds | Key points |
| --- | --- | --- |
| presentation | Every proof shown: verifier, | The person's audit trail. |
|   | attributes, mode (proof/reliance), |   |
|   | granted or denied, time, transfer |   |
|   | flag |   |
| consent | Person, verifier, scope, purpose, | First-class record, not a flag. |
|   | lawful_basis (consent, legal |   |
|   | obligation, contract), granted or |   |
|   | revoked, expiry, notice version |   |
| verifier | Registered relying party: name, | Mirrors EUDI relying-party |
|   | jurisdiction, public key, | registration. |
|   | registered purposes, max |   |
|   | attribute set, regulated-entity |   |
|   | flag |   |
| issuer_source | Which rail produced each fact: | Provenance. |
|   | DigiLocker, Aadhaar offline, EUDI, |   |
|   | eID, bank |   |
| access_log | Pseudonymous ID, verifier, | Not linked by foreign key; |
|   | outcome, time, region | survives erasure. |
| anchor_batch | Merkle root, hash-based | Optional. |
|   | signature, chain tx, block |   |
| key_epoch | Algorithm, parameter set, KMS | Which crypto protected |
|   | key and version, active from and | which row. |
|   | until |   |
| kyc_record_ref | Pointer to the regulatory record: | Layer B reference (section |
| [New] | owning regulated entity, method | 3.6). |
|   | (V-CIP, document, CKYCR), |   |
|   | evidence location, retention end, |   |
|   | legal hold |   |
| retention_rule | Per record type and country: | Feeds the retention engine. |
| [New] | legal period, purpose period, |   |
|   | trigger |   |
| status_list [New] | Bitstring per issuer and purpose | Many credentials per bit list |
|   | for revocation | for herd privacy. |


## 3.5 Cryptography

| Purpose | Choice |
| --- | --- |
| Facts at rest | AES-256-GCM, one DEK per fact, wrapped by a |
|   | KMS symmetric key with the subject ID as |
|   | additional authenticated data |
| Credential format | SD-JWT VC (selective disclosure by salted |
|   | hashes). ISO mdoc profile later for EU |
|   | interoperability |
| Signing, post-quantum profile ML-DSA-87 through KMS |   |
| Signing, EUDI profile | ES256 (conventional) to match current EU wallet |
|   | formats. Verify the current Architecture Reference |
|   | Framework. |
| Holder binding | Device-bound key (WebAuthn passkey) signing a |
|   | key-binding proof over the verifier's nonce and |
|   | audience |
| Anchor signature | Hash-based (SLH-DSA) in application code |
| Transport | TLS with hybrid ML-KEM where supported |
| Linking hashes | Keyed (HMAC with a per-record secret), so |
|   | destroying the secret breaks linkability (crypto- |
|   | shredding) |
| Rotation | Re-wrap DEKs on KMS key rotation; never re- |
|   | encrypt facts |

BBS+ is avoided because it is not quantum safe. Zero-knowledge proofs are an optional later layer.

## 3.6 Two-layer storage

Layer A: credential and consent layer (erasable, person-controlled). Encrypted facts, credentials, consents, presentation history. The person can delete it. Deleting destroys the per-fact keys.


Layer B: regulatory record (retention-locked). The CDD file a regulated entity must keep: identity evidence, V-CIP recording, screening results, risk rating. It is held either in the regulated entity's own systems (preferred, we hold only a reference) or in a dedicated retention vault run for the entity as processor. Retention follows PMLA (about 5 years after the relationship ends) in India and AMLR Article 77 (5 years, then deletion, unredacted) in the EU. Neither the person's erase button nor the self-destruct timer can delete Layer B before its date.

The erasure screen tells the truth per record: "Erased" or "Kept under PMLA until DATE" or "Kept under AMLR until DATE".

## 3.7 Chain role

- Once a day the anchor service builds a Merkle tree over that day's credential and consent hashes (keyed, high entropy), signs the root with a hash-based signature, and writes only the root.

- Revocation is off chain, using status lists.

- A person can prove a record existed on a given day by revealing their leaf and path.

- If the chain is dropped, replace it with a permissioned transparency log. The product does not depend on it.

- Cut order: the chain is the first thing to cut if time is short.

## 3.8 Security and operations

- Identity and access: least-privilege roles per service, separate KMS keys per purpose, no shared keys across cells.

- Secrets: managed secret store, injected by reference, never in config or images.

- Network: private database, no public IP, service-to-service auth.

- Logging: application and key-use audit logs. India cell retains 180 days in India. Access logs are pseudonymous; the log key is separate from the data key.

- Backups: encrypted; restoration tested; crypto-shredded keys must also expire in backups.

- Monitoring: alerts on key misuse, signing spikes, failed presentations, abnormal consent revocations.

- Incident clocks (one runbook): CERT-In 6 hours; GDPR 72 hours to the authority; DPDP Board and individuals per Rule 7 (verify); RBI reporting for banks.


- Resilience: multi-AZ database, tested recovery objectives. Contract terms for DORA (EU banks) and RBI outsourcing rules (Indian banks).

- Pen test and independent audit: required before any bank pilot.

## 4. How it works once live

## 4.1 Person onboarding, India

- 1. Person opens the vault app and signs in. A passkey (holder key) is created on their device.

- 2. Person picks a source: DigiLocker, Aadhaar offline XML (with their share code), or a bank-issued KYC.

- 3. The issuer adapter fetches or receives the document and verifies its signature (government certificate for XML).

- 4. The adapter extracts only the needed attributes (name, date of birth, state, PIN, ID type). The Aadhaar number is never stored; a salted reference key is.

- 5. Each attribute is encrypted separately and stored in attribute with its own wrapped key and an issuer_source entry.

- 6. The credential service issues a credential with assurance level and next_update_due , signs it (PQ profile), and puts it in the person's wallet.

- 7. If the person arrived through a bank, the bank (not KYCVault) performs CDD and uploads to CKYCR. KYCVault records the KYC Identifier in kyc_record_ref .

## 4.2 Person onboarding, EU

- 1. Person signs in; passkey created.

- 2. Person imports from the EUDI Wallet (PID), a national eID, or a bank-verified record.

- 3. The adapter verifies the issuer's signature and trust list status.

- 4. Facts are encrypted and stored in the EU cell. Credential issued in the EUDI- compatible profile, with a PQ profile for non-EU-wallet verifiers.

- 5. kyc_record_ref points to the obliged entity's CDD file when a bank was the issuer.

## 4.3 A bank as issuer (first KYC)

- 1. Bank staff open the Issuer console and start a KYC case.


- 2. The bank performs its own CDD (documents, V-CIP or eID, screening, risk rating). KYCVault does not replace this.

- 3. The bank approves. The credential service issues a credential tied to the bank as issuer, with cdd_level , risk category, method and next_update_due .

- 4. The CDD file stays in Layer B (bank's systems or retention vault). Only a reference and the facts the person agrees to hold go into Layer A.

- 5. India: bank uploads to CKYCR. EU: bank keeps the file for its five-year period.

## 4.4 Reuse by a second institution

- 1. The verifier console sends a presentation request: which attributes, purpose, mode (proof or reliance), and a nonce.

- 2. The policy engine checks the request against the verifier's registered purposes and maximum attribute set. Anything outside is rejected (code-level purpose limitation).

- 3. The person's app shows the request in plain language: who is asking, what is shared, why, for how long, and whether the verifier is outside their region.

- 4. Person approves. A consent is created with purpose, lawful basis and expiry.

- 5. Proof mode: the wallet reveals only the chosen salted attributes and adds a holder- binding proof. Reliance mode: the wallet also releases the CDD record reference or file under a signed consent.

- 6. The verifier checks: issuer signature and trust, status list, expiry, nonce and audience, holder binding, and that attributes match its request.

- 7. The verifier stores only a receipt (credential ID, scope, result, time) unless the law requires it to keep more (a regulated entity relying on CDD).

- 8. A presentation row and an access_log row are written.

## 4.5 Hotel or platform check (proof mode)

The desk shows a QR. The guest's phone shows "The hotel is asking: your name and that you are over 18". On approval the hotel sees a signed yes, the name, and nothing else. The guest's vault logs the request.

## 4.6 Revocation and withdrawal

- 1. Person revokes a consent in the app.


- 2. The consent service marks it revoked and stops all future presentations for that verifier and purpose.

- 3. A withdrawal notice goes to the verifier. By contract the verifier must delete data it no longer needs; legal retention duties remain.

- 4. If the credential itself is revoked (issuer or person), the status list bit flips and verifiers see it on their next check.

- 5. The UI states plainly that revocation cannot recall data already disclosed.

## 4.7 Expiry and re-verification

- next_update_due follows the issuer's cycle: India by risk (high 2, medium 8, low 10 years), EU at least yearly for high risk and five years otherwise.

- 90, 30 and 7 days before, the person and issuer are notified.

- At expiry, presentations fail with a clear "update required" status. The person re- verifies through the issuer, and a new credential supersedes the old.

## 4.8 Erasure request

- 1. Person requests erasure of the vault or of one fact.

- 2. The retention engine lists every record and its status: erasable now (Layer A), held under law until DATE (Layer B), or on legal hold.

- 3. Erasable data is crypto-shredded: per-fact DEKs and keyed-hash secrets are destroyed. Backups age out.

- 4. Held data stays locked, shown to the person with the legal reason, and deletes automatically at its date.

- 5. access_log remains in pseudonymous form for audit.

- 6. The person receives a confirmation they can keep.

## 4.9 Cross-border presentation

When a verifier is in another region, the app shows an "outside your region" notice and asks explicit consent for that presentation. Only the minimum attributes are sent. The verifier is bound by contract (SCCs where EU data goes to India) (verify transfer mechanism with counsel).


## 4.10 Audit and regulator access

- The person sees every access in their audit screen.

- The compliance console exports signed evidence bundles (issuer certificates, timestamps, consent versions, integrity hashes) for court or regulator use.

- Verifiers and regulators can verify the anchor root for any day without seeing personal data.

## 4.11 Incident handling

Detection alerts trigger the runbook. The compliance owner starts all legal clocks at once, decides which authorities and individuals to notify, and records decisions in the compliance console.

## 5. Step-by-step implementation plan

Durations are indicative for a small team. Each phase ends with a Done when test.

## Phase 0: Protect what exists (week 1)

- 1. Copy the 8 Sept database dump and the repo to two more locations.

- 2. Tag the current code. Freeze the old Sepolia contract; do not add data.

- 3. Write down the decisions D1 to D7 as signed-off design notes.

Done when: backups verified and decisions agreed.

## Phase 1: Foundation (weeks 1 to 3)

- 1. Create the India cell on AWS (Mumbai): VPC, private Postgres, KMS keys (symmetric, ML-DSA-87, ES256), secret store, logging.

- 2. Port the Terraform from GCP patterns. Keep separate keys per purpose.

- 3. Create the new Prisma schema (section 3.4). Migrate cleanly on an empty database.

- 4. Add the retention and key_epoch tables from day one.

Done when: a fact can be encrypted, stored, read back and its key epoch queried.


## Phase 2: Core services (weeks 3 to 6)

- 1. Split the monolith into modules: auth, issuer adapters, credential, consent, presentation, policy, retention, audit.

- 2. Move envelope encryption ( crypto.ts ) to per-fact use with subject-ID AAD.

- 3. Rebuild consent with purpose, basis, expiry and revocation.

- 4. Build the policy engine with the India rules file.

- 5. Remove the self-destruct sweep for any record with a retention rule.

Done when: a consent can be created, checked and revoked, and a retention rule blocks deletion.

## Phase 3: Credentials (weeks 5 to 8)

- 1. Implement SD-JWT VC issue and verify.

- 2. Sign with ML-DSA-87 via KMS (PQ profile). Verify signatures in the verifier SDK.

- 3. Add the ES256 EUDI profile (verify against the current ARF).

- 4. Add holder binding with passkeys and the key-binding proof.

- 5. Implement status lists and expiry fields.

Done when: a verifier validates a selectively disclosed credential end to end, including revocation.

## Phase 4: India integrations (weeks 6 to 10)

- 1. Aadhaar offline XML adapter: verify UIDAI signature offline; store derived attributes only. Verify the obligations for entities that rely on offline verification.

- 2. DigiLocker adapter against the requester API sandbox; submit onboarding with API Setu; use an aggregator in the interim.

- 3. Bank-issued KYC flow with CKYCR reference fields. The bank does the CKYCR upload.

- 4. Replace OCR as the primary path; keep it as a fallback.

Done when: a person is onboarded from the sandbox and receives a credential without any Aadhaar number stored.


## Phase 5: Frontends (weeks 6 to 10)

- 1. Person vault: facts held, consents, requests, audit, erasure with status per record, expiry reminders.

- 2. Verifier console: register, request, receive, receipts.

- 3. Issuer console: KYC case, approve, issue.

- 4. Compliance console: retention schedules, holds, export.

- 5. Side-by-side screen (whole document versus one fact) retained for demos.

Done when: every flow in section 4 runs through the UI.

## Phase 6: EU cell and EU integrations (weeks 9 to 14)

- 1. Stand up the EU cell in Frankfurt from the same code with the EU rules file.

- 2. Build the EUDI PID import and eID adapters against test frameworks.

- 3. Add relying-party style registration fields to the verifier registry.

- 4. Add cross-border notice and consent.

- 5. Draft DPIA, processor templates and transfer assessment.

Done when: the same person flow runs in both cells with their own rules.

## Phase 7: Chain and anchor (optional, weeks 12 to 14)

- 1. Replace KYCVault.sol with a root-anchor contract (write one root per day).

- 2. Remove per-person hashes and the per-person consent bits from chain.

- 3. Run the daily anchor job; add the leaf-and-path proof tool.

Done when: a root is on chain and a person can prove a leaf, with no personal data on chain.

## Phase 8: Compliance hardening (weeks 12 to 16)

- 1. Retention engine tests: legal hold, expiry deletion, erasure with held records.

- 2. Incident runbook rehearsal with all legal clocks.

- 3. Logging and 180-day retention in India verified.

- 4. Contract templates: bank processor terms, verifier terms with withdrawal-notice duty.

- 5. Third-party penetration test and independent security audit.


Done when: audit findings are closed and the compliance matrix is signed.

## Phase 9: Pilot (weeks 16 onward)

- 1. One regulated Indian entity as issuer, a second as relying verifier.

- 2. One EU pilot only when a relying party can accept wallet credentials.

- 3. Weekly review of consent, retention and incident logs.

## 6. Migration of the current API

| Current endpoint | New behaviour |   |
| --- | --- | --- |
| POST /api/ocr/extract | Fallback only. Primary path is issuer adapters. |   |
| POST /api/kyc/verify | Split into | POST /v1/issuers/{rail}/import and |
|   | POST /v1/credentials . |   |
| POST /api/consent/grant | POST /v1/consents with purpose, basis, scope, |   |
|   | expiry. |   |
| POST /api/consent/revoke | DELETE /v1/consents/{id} plus withdrawal |   |
|   | notice. |   |
| GET /api/kyc/access/:id | POST /v1/presentations (verifier request, |   |
|   | person approval, proof). |   |
| POST /api/otp/generate and | Kept as in-person QR/OTP presentation channel. |   |
| /verify |   |   |
| GET /api/kyc/me | GET /v1/vault . |   |
| GET /api/audit/:id | GET /v1/audit . |   |
| POST /api/kyc/set-expiry | Removed for regulated records. Optional only for |   |
|   | Layer A facts. |   |
| DELETE /api/kyc/forget | POST /v1/erasure-requests , handled by the |   |
|   | retention engine. |   |

New endpoints: GET /v1/credentials/{id}/status , GET /v1/status-lists/{id} , POST /v1/verifiers (registration), GET /v1/retention/{recordId} , POST /v1/legal- holds , GET /v1/anchors/{date} , GET /v1/evidence/{presentationId} .


## 7. Roles and permissions

| Role | Can do | Cannot do |
| --- | --- | --- |
| Person | View vault, grant and revoke | Delete regulated records before |
|   | consent, request erasure, view | their date |
|   | audit |   |
| Issuer (regulated | Run KYC cases, issue and revoke | Read other issuers' files |
| entity) | credentials |   |
| Verifier | Request attributes within | Ask for more than registered |
|   | registered scope, check proofs | scope; store more than the law |
|   |   | requires |
| Compliance | Manage retention rules, holds, | Read plain-text personal data |
|   | exports |   |
| Admin | Operate infrastructure | Use or export data keys |

## 8. Compliance controls by feature

| Feature | Law it serves |
| --- | --- |
| Per-fact encryption and crypto- | DPDP security and erasure; GDPR Arts 25, 32 |
| shredding |   |
| Purpose and basis on every consent | DPDP notice and consent; GDPR Arts 5, 6, 7 |
| Two-layer storage and retention engine | PMLA s.12; AMLR Art 77; GDPR Art 17(3)(b); |
|   | DPDP erasure subject to law |
| No Aadhaar number stored | Aadhaar Act and regulations |
| Daily root only on chain | EDPB blockchain guidelines |
| Status lists | GDPR minimisation |
| Registered verifier scope | eIDAS relying-party transparency; purpose |
|   | limitation |
| Cross-border notice | DPDP transfers; GDPR Chapter V |


| Feature | Law it serves |
| --- | --- |
| next_update_due | RBI periodic updation; AMLR update cycle |
| Evidence export | Bharatiya Sakshya Adhiniyam ss.61, 63 (verify) |
| Incident runbook | CERT-In, GDPR Art 33, DPDP breach rules |

## 9. Testing and acceptance

- Privacy test: an automated script checks that a verifier's stored data matches the receipt field list and no personal fields appear.

- Retention test: erasure of a record under legal hold must fail with the correct reason and date; at expiry it must delete.

- Crypto test: signature verification for both profiles, tamper detection, key rotation without re-encrypting facts.

- Policy test: a verifier asking beyond its registered scope is rejected.

- Region test: a person from each cell completes a flow, and no data appears in the other cell.

- End-to-end test: onboarding, issue, present, revoke, expiry, erasure, in both cells.

- Load and failover test: database failover, KMS throttling, DigiLocker outage (new sign- ups stop, existing credentials still work).

- Security review: third-party test and audit before any bank pilot.

## 10. Open decisions and risks

| Item | Question | Owner |
| --- | --- | --- |
| Cloud | Final move from GCP to AWS, and cost of two cells | Infra |
| Legal role | Processor or controller per feature; EU | Compliance |
|   | representative; grievance officer and DPO |   |
| EUDI profile | Exact credential formats and signature algorithms | Crypto |
|   | required by the current framework |   |
| Aadhaar offline | Obligations when relying on offline verification | Compliance |
| DigiLocker | Requester onboarding timeline; aggregator route | Compliance |


| Item | Question | Owner |
| --- | --- | --- |
| CKYCR | Access path as a technology provider | Compliance |
| Retention vault | Do we host Layer B for banks or only reference it? | Product |
| Chain | Keep a daily-root anchor or replace with a | Crypto |
|   | transparency log |   |
| Audit | Budget and timing for independent audit | Founders |
| Single operator key Multi-party control for any remaining chain writes Crypto |   |   |

What not to claim: no "GDPR compliant" or "DPDP compliant" until audited; no "quantum- safe blockchain"; no "integrated with DigiLocker" before onboarding; no replacement of V- CIP, CKYCR or regulated-entity duties.

Sources to verify before building: RBI KYC Master Direction (2025 amendments), PMLA and PML Rules, DPDP Act and Rules, UIDAI regulations, EUR-Lex texts (GDPR, eIDAS 2.0, AMLR Articles 22 and 77), the EUDI Architecture Reference Framework, AMLA draft standards, and AWS KMS post-quantum documentation.
