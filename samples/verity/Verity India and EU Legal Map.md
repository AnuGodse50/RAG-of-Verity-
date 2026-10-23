# Verity:  India and EU Legal Map

Team CodeVerse · Prepared 20 October 2026

**What this is:** a plain-English list of the main Indian and European laws that touch a reusable, privacy-preserving KYC product, what each one means, where the two regimes clash, and how to design around the clashes.

**Please note:** this is a planning guide, not legal advice. Dates were checked against recent commentary, but section numbers marked "verify" should be confirmed against the official Gazette (India) or EUR-Lex / EDPB (EU) before you rely on them.

## How to read this

- **Part 1** covers India, law by law.
- **Part 2** covers the EU, law by law.
- **Part 3** is the "base" of things that do not line up between the two, with a suggested fix for each.
- **Part 4** is a short timeline and a to-do list.

Three words that appear everywhere:

- **Personal data:** any information that relates to an identifiable person. A name, an ID number, and often even a hash or random ID that can be traced back to someone.
- **Controller / Data Fiduciary:** the party that decides why and how personal data is used. ("Controller" is the EU word, "Data Fiduciary" is the Indian word.)
- **Processor / Data Processor:** a party that handles data on behalf of a controller, following its instructions.

# Part 1. India

## 1.1 Privacy and data protection

### Digital Personal Data Protection Act, 2023 (DPDP Act)

**In simple words:** India's main privacy law. It says anyone handling the personal data of people in India must have a lawful reason, tell people clearly what they are doing, protect the data, and respect people's rights.

**Key terms it defines:**

- *Data Principal:* the person the data is about.
- *Data Fiduciary:* whoever decides the purpose and means of processing (a bank, or KYCVault for the user's vault).
- *Data Processor:* whoever processes on a fiduciary's behalf.
- *Consent Manager:* a registered intermediary that lets a person give, review and withdraw consent in one place.
- *Significant Data Fiduciary:* a fiduciary of high volume or high risk (financial data, large scale) that faces extra duties: independent audit, impact assessments and a data protection officer.

**What it asks of us:**

- Notice in clear language before collecting data, stating the data and the purpose.
- Consent that is free, specific, informed and unambiguous, and as easy to withdraw as to give. Consent is not the only basis. The Act also lists "legitimate uses", which include complying with a legal obligation (verify the exact section; the Legal Aspects sheet cites s.7 for consent, but consent appears to be s.6 and legitimate uses s.7).
- Reasonable security safeguards and breach reporting.
- Erase data when the purpose is over or consent is withdrawn, unless another law requires keeping it.
- Rights to access, correction, erasure and grievance redress.
- Verifiable parental consent for children's data.
- Limits on moving data abroad (the government can restrict specific countries).
- Penalties of up to ₹250 crore for serious breaches.

**Status:** the Act and Rules took effect in stages. Recent commentary says the Consent Manager provisions arrive on 13 November 2026 and the main operative rules and penalties on 13 May 2027.

### Digital Personal Data Protection Rules, 2025

**In simple words:** the detailed instructions for running the Act: what a notice must contain, how Consent Managers register (an Indian company with ₹2 crore minimum net worth), what "reasonable security" means, how fast to report a breach, how long to keep logs, how children's consent is verified, and extra duties for Significant Data Fiduciaries. Verify rule numbers (for example, Rule 4 on Consent Managers and Rule 7 on breach reporting).

### Information Technology Act, 2000 (IT Act)

**In simple words:** India's core cyber law. It gives legal validity to electronic records and signatures, punishes hacking and data theft, protects intermediaries under conditions, and lets the government order interception or decryption under defined rules. Section 43A (compensation for failing to protect sensitive data) is due to be removed when the DPDP operative date arrives on 13 May 2027.

### Information Technology (Reasonable Security Practices and Sensitive Personal Data or Information) Rules, 2011 (SPDI Rules)

**In simple words:** the older privacy rules. They treat financial information, passwords and some identity data as "sensitive", and require consent, a privacy policy and reasonable security. Treat them as a parallel baseline until DPDP fully replaces them.

### CERT-In Directions, 2022

**In simple words:** cyber-incident rules. Report specified incidents to CERT-In within **6 hours**, keep ICT logs for a rolling **180 days**, and keep them within India. Your logging design must support this.

## 1.2 Anti-money-laundering and KYC

### Prevention of Money Laundering Act, 2002 (PMLA)

**In simple words:** the law against money laundering. "Reporting entities" (banks, financial institutions, intermediaries) must identify customers, keep records of identity and transactions, and report suspicious activity to FIU-IND.

**What matters to us:** Section 12 requires keeping transaction records and client identity records, generally for **five years** after the transaction or after the relationship ends. Early deletion is not allowed. This is the main collision with privacy erasure.

### Prevention of Money-laundering (Maintenance of Records) Rules, 2005 (PML Rules)

**In simple words:** the detailed rulebook under PMLA. It defines customer due diligence (CDD): identify the customer, find the beneficial owner, verify with approved documents, and keep records. It also covers the Central KYC Records Registry (CKYCR). Rule 9 is the key CDD rule.

### RBI Master Direction on KYC, 2016

**In simple words:** the Reserve Bank's KYC rulebook for banks and similar regulated entities. It sets the Customer Acceptance Policy, Customer Identification, ongoing monitoring, risk categories, and the approved ways to verify identity: officially valid documents, Aadhaar e-KYC, CKYC retrieval, digital KYC, and Video-based CIP (V-CIP).

**Points that bite us:**

- The **receiving bank stays responsible** even when it relies on someone else's verification.
- V-CIP is a live, secure, auditable process. A static credential or a proof is not equal to it.
- KYC must be **periodically refreshed** on a risk basis (verify the intervals: roughly 2 years high-risk, 8 years medium-risk, 10 years low-risk).
- Regulated entities must upload to and retrieve from CKYCR.

The RBI consolidated many directions in late 2025, so check the current document title and paragraph numbers.

### CERSAI / Central KYC Records Registry (CKYCR)

**In simple words:** the national registry where KYC records are stored once and fetched by other regulated entities using a KYC identifier. CERSAI was set up under the SARFAESI Act, 2002. Your system should connect to it, never replace it.

### Sector regulators: SEBI, IRDAI, PFRDA

**In simple words:** securities, insurance and pension regulators each have their own KYC rules. SEBI uses KYC Registration Agencies (KRAs). A credential from us can help these regulated entities but cannot replace their sector process.

### RBI Account Aggregator framework

**In simple words:** India's existing system for consent-based financial data sharing, where a regulated aggregator moves data only when the person approves a specific consent request. It is the best local example of the consent design we want, so copy its shape.

### RBI outsourcing / cloud directions

**In simple words:** banks must keep control and audit rights over vendors that handle their data. Expect banks to pass these terms on to us in contracts.

### Virtual Digital Asset (VDA) AML notification, 2023

**In simple words:** certain crypto service providers became PMLA reporting entities. Because we use a blockchain, keep the product clearly separate from exchange, transfer or custody services.

## 1.3 Identity systems and evidence

### Aadhaar Act, 2016, with the Authentication and Offline Verification Regulations, 2021 and the Sharing of Information Regulations

**In simple words:** the law behind Aadhaar. It restricts who may use Aadhaar and for what. Biometrics cannot be stored or shared, the Aadhaar number cannot be freely kept or passed on, and use needs consent and a stated purpose.

**What matters to us:** do not put an Aadhaar number, XML or biometrics on a chain. Hashing an Aadhaar number does not make it safe. If you use Paperless Offline e-KYC, verify the signature, keep only the minimum derived attributes, and check what obligations apply to entities that rely on offline verification.

### DigiLocker rules (Digital Locker Facilities Rules, 2016) and API Setu

**In simple words:** DigiLocker is the government's document wallet. Businesses that want to fetch documents ("requesters") must be formally onboarded through API Setu with a signed agreement. Until then, say "sandbox" or go through a licensed aggregator.

### Bharatiya Sakshya Adhiniyam, 2023 (Evidence Act replacement)

**In simple words:** electronic records are valid evidence, but only if their origin and integrity can be shown (see sections 61 and 63, verify). Keep issuer keys, timestamps, consent records and system integrity details so a credential or log can stand up in court.

# Part 2. Europe (EU)

## 2.1 Privacy and data protection

### General Data Protection Regulation, 2016/679 (GDPR)

**In simple words:** the EU's privacy law. It applies to anyone handling data of people in the EU, including firms outside the EU that offer them services. Fines can reach 4% of global annual turnover or €20 million, whichever is higher.

**Key terms (Article 4):**

- *Personal data:* any information about an identified or identifiable person. Pseudonymised data (identifiers replaced, but re-linkable) is still personal data. Only truly anonymous data is outside the law.
- *Controller / Processor:* as defined above.
- *Consent:* freely given, specific, informed and unambiguous, with a clear affirmative action.

**What it asks of us:**

- **Principles (Art 5):** lawfulness, purpose limitation, data minimisation, accuracy, storage limitation, security, accountability.
- **Legal basis (Art 6):** consent, contract, legal obligation, and others. For bank KYC the usual basis is legal obligation, not consent.
- **Consent rules (Arts 7–8):** easy to withdraw; special rules for children.
- **Special data (Art 9):** biometric data used to identify someone gets extra protection.
- **Rights (Arts 12–22):** access, correction, erasure, restriction, portability, objection, and protection from purely automated decisions (Art 22).
- **Erasure exception (Art 17(3)(b)):** you may keep data when a legal obligation requires it.
- **Design duties:** data protection by design and default (Art 25), processor contracts (Art 28), records of processing (Art 30), security (Art 32).
- **Breaches:** notify the regulator within 72 hours (Art 33), and affected people when the risk is high (Art 34).
- **Impact assessment (Art 35):** needed for large-scale or high-risk processing. Assume it applies to us.
- **Data protection officer (Arts 37–39).**
- **Transfers outside the EU (Arts 44–49):** need an adequacy decision, Standard Contractual Clauses plus a transfer impact assessment, or a narrow exception such as explicit consent. As far as I know, India has no adequacy decision, so verify.
- **Non-EU firms (Art 27):** may need an EU representative.

### EDPB Guidelines 02/2025 on blockchain (final version adopted 7 July 2026)

**In simple words:** the EU regulators' board explains how GDPR applies to blockchains. The headline: avoid putting personal data on chain, and hashed or encrypted data can still be personal data. Immutability does not excuse a controller from erasure and other rights. If something must go on chain, the guidelines discuss mitigation techniques with trade-offs, and they expect a good reason.

### Other EDPB guidance to know

- Guidelines on data protection by design and default (Art 25).
- Guidelines on consent, and on controllers and processors.
- Guidelines on pseudonymisation.
- Draft anonymisation guidelines (consultation open until 30 October 2026), important for deciding whether salted hashes or commitments are really anonymous.

## 2.2 Digital identity

### eIDAS 2.0 (Regulation 2024/1183) and the EUDI Wallet framework

**In simple words:** a law creating the EU Digital Identity Wallet: a free, citizen-controlled app holding verified identity data (the Person Identification Data, PID) and attestations (such as "over 18"). It is built for selective disclosure. Verifiers ("relying parties") must register and declare what data they request.

**Dates:** member states must offer a wallet by late December 2026, and regulated entities such as banks must accept wallets by December 2027.

**Technical profile:** the EU Architecture Reference Framework points to SD-JWT VC and ISO mdoc credential formats. Check the current version for signature algorithm requirements.

## 2.3 Anti-money-laundering

### Anti-Money Laundering Regulation, 2024/1624 (AMLR)

**In simple words:** a single EU rulebook for customer due diligence, replacing the patchwork of national rules. It applies from **10 July 2027**. It recognises qualifying electronic identification, including wallet credentials, as a way to verify identity, subject to technical standards. It sets record retention (generally five years after the relationship ends, verify) and rules for relying on other firms' due diligence.

### AMLA Regulation 2024/1620 and the 6th AML Directive 2024/1640

**In simple words:** these create the EU Anti-Money Laundering Authority (AMLA), which is preparing direct supervision of high-risk firms from 2028, and update national supervisors' powers. AMLA is also writing the technical standards for customer due diligence.

### EBA Guidelines on remote customer onboarding

**In simple words:** the banking authority's rules for onboarding customers digitally without meeting them, including how to check documents, liveness, and the reliability of the technology used.

## 2.4 Security, operations and AI

### Digital Operational Resilience Act, 2022/2554 (DORA)

**In simple words:** financial entities must manage ICT risks and tightly control third-party technology vendors. If a bank uses KYCVault, we become an ICT third-party provider. Expect contract requirements on audit access, incident reporting, exit plans and subcontractors.

### NIS2 Directive, 2022/2555

**In simple words:** a cybersecurity law for important and essential sectors, including digital infrastructure and trust services. It may apply to us directly, depending on our size and activity.

### AI Act, 2024/1689

**In simple words:** rules for AI systems by risk level. It matters if we add face matching or liveness detection. Confirm how biometric verification is classified before building.

### Digital Omnibus (proposal)

**In simple words:** a proposed EU package that could adjust GDPR and related rules. I have not verified its current status. Track it.

### National laws

Member states add their own AML, banking and data-protection details. Once you pick a first EU country, map its national rules too.

# Part 3. Where the two do not align, and how to fix it

This is the "base" of mismatches. For each: what India says, what the EU says, why it clashes, and a suggested design answer.

## 3.1 Deleting data versus keeping records

- **India:** DPDP gives a right to erasure, but PMLA requires banks to keep identity and transaction records for about five years after the relationship ends.
- **EU:** GDPR gives a right to erasure, but allows keeping data to meet a legal obligation. AMLR also requires retention.
- **Clash:** your old "forget" button and 7-day self-destruct timer would delete records banks are legally required to keep.
- **Suggestion:**
  1. Split storage into two layers: a **regulatory record** held for the regulated entity with a retention lock, and a **credential and consent layer** the user can erase.
  2. Add a retention engine: keep each record until the longer of the legal period and the purpose period, per country, with a legal-hold flag.
  3. Make the erasure screen honest: "Erased" or "Kept under PMLA until DATE".
  4. Remove the self-destruct timer for bank-linked records.

## 3.2 Consent versus legal obligation

- **India and EU:** a bank's KYC is justified by law, not by the customer's consent. Yet both regimes expect people to control sharing of their data.
- **Clash:** if the app lets "withdraw consent" appear to delete a legally required record, it misleads the user. If a bank treats consent as its basis, withdrawal could break its compliance.
- **Suggestion:**
  1. Give every consent record a `lawful_basis` field (consent, legal obligation, contract) alongside purpose, recipient, scope, expiry and country.
  2. Make withdrawal stop *future* disclosures and flip revocation status. State clearly that it cannot recall data a verifier must legally keep.
  3. Model consent on the Account Aggregator style, and stay compatible with a DPDP Consent Manager.
  4. Send verifiers a withdrawal notice and require, by contract, that they delete data they no longer need.

## 3.3 Blockchain immutability

- **India:** DPDP's correction and erasure rights apply; the project's own notes say no identifying KYC data should be on chain.
- **EU:** EDPB's final guidelines say hashes can still be personal data and immutability is no excuse.
- **Clash:** a per-person hash on a public chain cannot be corrected or erased.
- **Suggestion:**
  1. Put on chain only a **daily Merkle root** built from salted, keyed leaves. Never one hash per person.
  2. Use a **status list** (one bit per credential, many per list) for revocation instead of per-person flags.
  3. Use per-record secrets so destroying the secret breaks linkability (crypto-shredding). Describe this as a protective measure, not anonymisation.
  4. Consider replacing the public chain with a permissioned transparency log. The disclosure story does not depend on a blockchain.

## 3.4 Moving data across borders

- **India:** DPDP allows transfers abroad except to countries the government restricts. Sector rules (RBI payment data, CERT-In logs) can require data or logs to stay in India.
- **EU:** transfers outside the EU need a legal mechanism. India has no adequacy decision, as far as I know.
- **Clash:** an EU person presenting a credential to an Indian verifier, or the reverse, is a cross-border flow.
- **Suggestion:**
  1. Keep the regional cells (India, EU) with no shared database.
  2. In the wallet, show "this verifier is outside the EU" and ask for explicit consent per presentation.
  3. Require SCCs and a transfer impact assessment with verifiers, and send only the minimum attribute.
  4. Never replicate stored data across regions.

## 3.5 The global pointer index

- **EU:** a random ID linked to a person, even if you cannot see their name, is pseudonymous personal data.
- **Clash:** the plan says the index holds "no personal data".
- **Suggestion:** either treat the index as personal data (document the basis, minimise, secure it), or remove it by routing from the credential issuer, or by per-region lookups.

## 3.6 Aadhaar limits versus "hash it and it is fine"

- **India:** Aadhaar rules restrict storing and sharing the number, and hashing does not cure unauthorised use.
- **EU:** hashes of identifiers are still personal data.
- **Suggestion:** accept both. Do not store the Aadhaar number, XML or biometrics. Keep only derived attributes (name, age flag, state) and a reference. Check offline-verification obligations before processing any Aadhaar XML.

## 3.7 Credential format versus post-quantum signatures

- **EU:** the EUDI framework uses specific formats (SD-JWT VC, mdoc) and conventional signature algorithms. Check the current framework version.
- **Plan:** sign everything with ML-DSA-87.
- **Clash:** an EU wallet or verifier may not accept a pure ML-DSA credential today.
- **Suggestion:** issue a **dual profile**: an EUDI-compatible credential with a conventional signature, plus an ML-DSA-signed version for your own network. Plan to move EU to post-quantum once the framework permits.

## 3.8 Proof of identity versus V-CIP and CDD

- **India:** a selective-disclosure proof is not a complete V-CIP. The receiving bank stays responsible. KYC must be refreshed on a risk cycle. CKYCR integration is required.
- **EU:** wallet credentials can support CDD, but only at the assurance level the technical standards require, and relying on others is limited.
- **Suggestion:**
  1. Issue credentials only after a regulated entity has done CDD.
  2. Put in each credential: CDD level, KYC date, risk category, next-update-due date and revocation endpoint.
  3. Build a CKYCR connector that the regulated entity operates. We stay a technology provider.
  4. Never market the credential as a replacement for V-CIP or sector KYC.

## 3.9 Breach and log rules

- **India:** CERT-In 6 hours; DPDP breach reporting to the Board and affected people (verify timings in Rule 7); logs for 180 days in India; PMLA records for five years.
- **EU:** 72 hours to the regulator; minimise stored logs.
- **Clash:** several clocks start at once, and logs are both required and a privacy risk.
- **Suggestion:** write one incident runbook with every clock in one table. Store pseudonymous access logs per region, with the log key separate from the data key.

## 3.10 Roles: who is the controller?

- **Both:** the controller/fiduciary carries the heaviest duties.
- **Clash:** for bank-driven KYC we act for the bank (processor). For the person-held vault we may be the controller. The plan blurs this.
- **Suggestion:** decide per feature, put it in processor contracts (GDPR Art 28 and DPDP processor terms), name a DPO / grievance officer, and appoint an EU representative if serving EU residents without an EU office.

## 3.11 Children and age proofs

- **India:** verifiable parental consent for children's data.
- **EU:** the age of digital consent varies by member state (13 to 16).
- **Suggestion:** keep a per-country age rule in the rules engine. Treat age proof as a product feature and a compliance feature.

## 3.12 Biometrics and automated decisions

- **EU:** biometric identification is special-category data; solely automated decisions have limits.
- **India:** Aadhaar biometrics cannot be stored or shared.
- **Suggestion:** do not store face templates. If liveness is added, keep it separate, use a clear lawful basis, and keep a human review route for risk decisions.

# Part 4. Dates and to-do list

| Date | What happens |
| --- | --- |
| 30 Oct 2026 | EDPB anonymisation guidelines consultation closes |
| 13 Nov 2026 | India: Consent Manager provisions commence |
| Late Dec 2026 | EU: wallets available in every member state |
| 13 May 2027 | India: main DPDP duties and penalties start; IT Act s.43A removed |
| 10 Jul 2027 | EU: AMLR applies |
| Dec 2027 | EU: regulated entities must accept wallets |
| 2028 | AMLA begins direct supervision |

**Documents to produce:**

1. A data protection impact assessment (needed in the EU, and expected for a Significant Data Fiduciary in India).
2. A retention schedule per country.
3. Processor and verifier contract templates.
4. A cross-border transfer assessment for EU-India flows.
5. A control-to-clause matrix linking each feature to the law behind it.
6. One incident runbook with all deadlines.

**Sources to verify before relying on anything above:** the India Gazette (DPDP Act and Rules, RBI directions), the PMLA text, EUR-Lex (GDPR, eIDAS 2.0, AMLR, DORA), and the EDPB website. Commentary from law firms and vendors is good for planning but not for contracts.
