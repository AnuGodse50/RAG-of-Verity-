# Verity RAG Test Questions and Reference Answers

This file pairs the 10 retrieval-evaluation questions in `verity_cases.json` with concise, source-grounded reference answers.

**Execution status:** these are reference answers prepared from the cited Verity source files; they are not captured outputs from a live RAG run. I attempted to run the evaluator, but the current Python environment is missing `PyYAML` (`ModuleNotFoundError: No module named 'yaml'`). Install the project dependencies and run the evaluator before treating these as observed agent responses.

## 1. India company documents

**Question:** What documents does the India KYC guide list for a company and its beneficial owners?

**Reference answer:** The guide lists a certificate of incorporation, memorandum and articles, PAN, a board resolution authorizing signatories, identity documents for officers and signatories, and identification of beneficial owners. It says ownership thresholds should be verified against the applicable rules, so this list should not be treated as confirmed customer-specific requirements without approved, current guidance.

**Source:** `samples/verity/KYC Process Guide India and Europe.md` — “Companies, firms and others,” page 6.

## 2. India individual identity and address evidence

**Question:** Which identity documents and address evidence are mentioned for individuals in India?

**Reference answer:** The guide lists passport, driving licence, proof of possession of an Aadhaar number, voter ID, NREGA job card, and a National Population Register letter as Officially Valid Documents. It also mentions recent utility bills, property tax receipts, and pension orders as examples of address evidence. The guide says to verify the current accepted list and age limits.

**Source:** `samples/verity/KYC Process Guide India and Europe.md` — “Documents needed in India,” page 5.

## 3. India record retention

**Question:** How long does the India guide say identity and transaction records are retained?

**Reference answer:** The guide says identity and transaction records must be kept for at least five years after the relationship ends or the transaction takes place. It also says the exact wording can differ by record type and should be verified.

**Source:** `samples/verity/KYC Process Guide India and Europe.md` — “Where the data is stored and for how long,” page 7.

## 4. EU central KYC registry

**Question:** Does the EU have a central KYC registry comparable to India's CKYCR?

**Reference answer:** The guide says there is no single central KYC registry in the EU comparable to India's CKYCR. It says each obliged entity keeps its own file, though some countries have national eID schemes or private utilities.

**Source:** `samples/verity/KYC Process Guide India and Europe.md` — “How KYC works in the EU today and from July 2027.”

## 5. Differences between EU countries

**Question:** Which KYC details vary by EU country, such as accepted IDs and verification deadlines?

**Reference answer:** The guide says national rules determine details such as accepted identity documents, whether video identification is allowed, verification deadlines, and national eID schemes. It recommends mapping the rules for the specific country.

**Source:** `samples/verity/KYC Process Guide India and Europe.md` — “How the process differs by country.”

## 6. Regional cells

**Question:** Where are the proposed India and EU regional cells located in the Verity architecture?

**Reference answer:** The architecture blueprint places the India cell in Mumbai and the EU cell in Frankfurt. It describes each as a separate deployment with its own database, keys, secrets, logs, and rules.

**Source:** `samples/verity/Verity System Process and Architecture Blueprint.md` — “Regional cells.”

## 7. Two-layer storage

**Question:** What are the two storage layers in the architecture, and what kind of data belongs in each?

**Reference answer:** Layer A is an erasable credential and consent layer for encrypted facts, credentials, consents, and presentation history. Layer B is a retention-locked regulatory-record layer for records a regulated entity must retain, such as identity evidence and verification records. The blueprint says Layer B is held by the regulated entity or in a dedicated vault run for it.

**Source:** `samples/verity/Verity System Process and Architecture Blueprint.md` — “Two-layer storage.”

## 8. Consent service

**Question:** What does the consent service do in the target system architecture?

**Reference answer:** The blueprint describes the consent service as creating, tracking, and revoking consents, with details such as purpose, recipient, lawful basis, scope, and expiry.

**Source:** `samples/verity/Verity System Process and Architecture Blueprint.md` — “Services.”

## 9. India's DPDP Act

**Question:** What does the India and EU legal map say about India's DPDP Act and personal data processing?

**Reference answer:** At a high level, the legal map says the Act requires a lawful reason for processing personal data, clear information about what is being done, reasonable security safeguards, and respect for people’s rights. The source itself flags details for verification; this summary is not legal advice.

**Source:** `samples/verity/Verity India and EU Legal Map.md` — “Digital Personal Data Protection Act, 2023 (DPDP Act).”

## 10. Cross-border data transfers

**Question:** What considerations does the legal map identify for moving personal data across borders?

**Reference answer:** The legal map says India may restrict transfers to countries named by the government and that sector rules can require certain data or logs to remain in India. It says EU transfers outside the EU need a legal mechanism. Its proposed architecture is to keep separate regional cells, request consent for cross-region presentations, minimize transferred attributes, and avoid replicating stored data across regions. These are points from the source document, not legal advice.

**Source:** `samples/verity/Verity India and EU Legal Map.md` — “Moving data across borders.”

## Run the retrieval evaluation

After installing dependencies and ingesting the Verity source files, run:

```powershell
rag ingest verity samples/verity
python -m evaluation verity evaluation/verity_cases.json --k 6
```

The evaluator reports retrieval hit rate@k and MRR. It does not generate answers; compare actual `/query` or `rag ask` output against the reference answers above separately.
