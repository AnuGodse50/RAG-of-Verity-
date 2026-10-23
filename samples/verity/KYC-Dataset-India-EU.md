# KYC Dataset: India and European Union  
## Processes, Documents, Data Attributes, and Use Cases

This document is a structured knowledge dataset for a KYC/KYB platform and RAG assistant. It covers KYC processes, required documents, customer data attributes, verification methods, risk categories, re-KYC rules, and major use cases in India and the European Union.

**Important:** This is a product and workflow dataset, not legal advice. Exact document lists, retention periods, thresholds, and compliance obligations must be validated with qualified legal and compliance teams for each market and institution.

---

# 1. KYC Basics

## 1.1 What is KYC?

KYC means **Know Your Customer**.

It is the process used by a regulated organization to:

- Identify a customer
- Verify the customer’s identity
- Verify the customer’s address
- Understand the purpose of the relationship
- Assess money-laundering and fraud risk
- Screen the customer against sanctions, PEP, and watchlist sources
- Monitor the relationship over time

## 1.2 KYC vs KYB

| Term | Meaning | Used for |
|---|---|---|
| KYC | Know Your Customer | Individual customers |
| KYB | Know Your Business | Companies, MSMEs, startups, trusts, NGOs, and other organizations |
| CDD | Customer Due Diligence | Identifying and verifying a customer |
| EDD | Enhanced Due Diligence | Higher-risk customers or transactions |
| AML | Anti-Money Laundering | Preventing money laundering |
| CFT | Countering the Financing of Terrorism | Preventing terrorist financing |
| PEP | Politically Exposed Person | A person with prominent public functions or their family/close associates |
| UBO | Ultimate Beneficial Owner | The natural person who ultimately owns or controls a business |
| Re-KYC | Reverification of KYC | Updating or refreshing an existing KYC record |

---

# 2. Core KYC Data Attributes

## 2.1 Individual KYC attributes

| Attribute | Example | Usually required |
|---|---|---|
| Full legal name | Rahul Sharma | Yes |
| Date of birth | 12 August 1998 | Yes |
| Gender | Male / Female / Other | Often |
| Nationality | Indian | Yes |
| Mobile number | +91-98XXXXXXXX | Yes |
| Email address | user@example.com | Often |
| Current residential address | Flat 402, MG Road, Bengaluru | Yes |
| Permanent address | Same as current address | Often |
| Photograph | Customer selfie or passport photo | Often |
| Identity document type | Aadhaar, PAN, passport, voter ID | Yes |
| Identity document number | Masked or tokenized reference | Yes |
| Document expiry date | 2030-05-20 | If applicable |
| PAN | ABCDE1234F | Often |
| Occupation | Software engineer | Often |
| Income range | INR 5–10 lakh per year | Sometimes |
| Source of funds | Salary, business income, savings | Sometimes |
| Tax residency | India | Sometimes |
| Politically exposed person status | Yes / No | Yes for risk assessment |
| Sanctions screening result | Clear / potential match / review required | Yes for regulated onboarding |
| Risk category | Low / medium / high | Yes |
| Verification status | Pending / verified / rejected / resubmission required | Yes |
| Verification date | 2026-10-23 | Yes |
| Assurance level | Basic / substantial / high | Yes |

## 2.2 Business KYB attributes

| Attribute | Example | Usually required |
|---|---|---|
| Legal business name | Acme Technologies Private Limited | Yes |
| Trade name | AcmeTech | Sometimes |
| Business type | Private Limited Company | Yes |
| Country of incorporation | India | Yes |
| Registration number | CIN / company number | Yes |
| Date of incorporation | 2020-04-15 | Yes |
| Registered address | Bengaluru, India | Yes |
| Operating address | Bengaluru, India | Often |
| Industry / sector | Software development | Yes |
| GSTIN / tax ID | Applicable tax identifier | Often |
| Business PAN | Business PAN | Often |
| Website | https://example.com | Often |
| Authorized representative | Name, role, identity | Yes |
| Directors | Names, identities, roles | Often |
| Shareholders | Names and ownership percentage | Often |
| Beneficial owners | Natural persons with ownership/control | Often |
| Business bank account | Account verification reference | Often |
| Expected transaction volume | Monthly/annual estimate | Sometimes |
| Source of funds | Revenue, investment, loans | Sometimes |
| KYB risk category | Low / medium / high | Yes |
| KYB status | Pending / verified / rejected | Yes |

---

# 3. KYC Process Flow

## 3.1 Individual KYC process

```text
Customer signs up
        |
        v
Customer provides mobile number / email
        |
        v
Customer selects verification method
        |
        v
Identity verification
        |
        v
Address verification
        |
        v
Risk assessment and screening
        |
        v
Manual review, if required
        |
        v
KYC approved / rejected / resubmission requested
        |
        v
KYC record created
        |
        v
Customer can reuse verified attributes with consent
```

## 3.2 Business KYB process

```text
Business representative signs up
        |
        v
Business details entered
        |
        v
Business documents uploaded
        |
        v
Directors and shareholders added
        |
        v
Beneficial owners identified
        |
        v
Associated persons complete KYC
        |
        v
Business screening and risk assessment
        |
        v
Manual review, if required
        |
        v
KYB approved / rejected / resubmission requested
        |
        v
KYB record created
```

## 3.3 Consent-based reusable KYC flow

```text
Customer completes KYC with Institution A
        |
        v
Customer receives verified attributes and assurance level
        |
        v
Institution B requests specific attributes
        |
        v
Customer reviews purpose and requested attributes
        |
        v
Customer approves or rejects request
        |
        v
Customer selects optional attributes to disclose
        |
        v
Platform issues one-time, request-specific proof
        |
        v
Institution B receives approved attributes and proof
        |
        v
Customer sees access event in history
        |
        v
Proof cannot be reused
```

---

# 4. KYC Document Dataset

## 4.1 India: Individual KYC documents

| Document | Used for | Commonly accepted for |
|---|---|---|
| Aadhaar card | Identity and address | Banks, NBFCs, insurance, mutual funds, telecom, government schemes |
| Aadhaar e-KYC | Identity and address | Banks, NBFCs, insurance, mutual funds, government services |
| PAN card | Identity and tax identification | Banks, investments, loans, high-value transactions |
| Passport | Identity and address | Banks, travel, insurance, investments |
| Voter ID | Identity and address | Banks, NBFCs, insurance |
| Driving licence | Identity and address | Banks, NBFCs, insurance |
| NREGA job card | Identity and address | Certain financial and government use cases |
| Utility bill | Address proof | Banks, NBFCs, insurance |
| Bank statement | Address proof | Banks, NBFCs, insurance |
| Passport-size photograph | Identity verification | Banks, insurance, investments |
| DigiLocker documents | Digital document verification | Banks, education, travel, government services |
| Video KYC recording | Identity and liveness verification | Banks and regulated entities where permitted |
| CKYC record | Reuse of existing KYC | Banks, NBFCs, insurers, mutual funds, brokers |

## 4.2 India: Address proof validity

| Document | Common validity requirement |
|---|---|
| Utility bill | Usually issued within the last 3 months |
| Bank statement | Usually issued within the last 3 months |
| Aadhaar | Subject to applicable verification rules |
| Passport | Usually valid / unexpired |
| Driving licence | Usually valid / unexpired |
| Voter ID | Subject to applicable verification rules |

## 4.3 India: Business KYB documents

| Document | Used for |
|---|---|
| Certificate of incorporation | Company verification |
| Memorandum of association | Company structure and objectives |
| Articles of association | Governance rules |
| Company PAN card | Tax identification |
| GST registration certificate | Tax and business verification |
| Partnership deed | Partnership firms |
| Trust deed | Trusts |
| Board resolution | Authorized signatories |
| Proof of registered address | Business address verification |
| Bank statement or cancelled cheque | Bank account verification |
| Shareholding pattern | Ownership verification |
| Beneficial-owner declaration | UBO identification |
| Director identification details | Director verification |
| MSME registration | MSME verification |
| Trade licence | Certain business types |
| Import-export certificate | Import/export businesses |

---

# 5. India KYC Methods

## 5.1 Aadhaar e-KYC

Aadhaar e-KYC allows a customer to verify identity electronically using Aadhaar-based authentication.

### Data typically returned

- Name
- Date of birth or age band
- Gender
- Address
- Photograph reference
- Aadhaar reference / masked Aadhaar
- Mobile-number verification status

### Platform use

The platform can receive verification results and issue a customer-approved proof without storing unnecessary raw Aadhaar data.

## 5.2 DigiLocker

DigiLocker allows users to store and share official digital documents.

### Common documents

- Aadhaar card
- PAN card
- Driving licence
- Vehicle registration certificate
- Insurance policy
- Marksheets
- Certificates

### Platform use

The customer can authorize sharing of a specific document or verified attribute with an institution.

## 5.3 Video KYC / V-CIP

Video KYC is a remote verification process using live video interaction.

### Typical checks

- Live customer presence
- Identity-document verification
- Facial match
- Liveness detection
- Geolocation or location checks, where applicable
- Random questions or declarations

### Platform use

The platform can orchestrate V-CIP through a regulated provider or bank and retain only approved result metadata.

## 5.4 CKYC

CKYC is India’s Central KYC Records Registry.

### Key concepts

| Term | Meaning |
|---|---|
| CKYC | Central KYC |
| CKYCRR | Central KYC Records Registry |
| KIN | KYC Identifier |
| KRA | KYC Registration Agency |

### CKYC-covered sectors

- Banks
- NBFCs
- Insurance companies
- Mutual funds
- Securities firms
- Pension funds
- Payment aggregators

### Platform use

A customer can complete KYC once and reuse the CKYC record across participating institutions with consent.

## 5.5 PAN verification

PAN verification is commonly used for:

- Bank accounts
- Investments
- Loans
- Credit cards
- High-value transactions
- Tax-related services

### Data verified

- Name
- PAN status
- Date of birth or incorporation
- Name match

---

# 6. India KYC Use Cases

## 6.1 Bank account opening

| Item | Details |
|---|---|
| Use case | Open savings, current, salary, NRE, or NRO account |
| Customer type | Individual or business |
| Core documents | Aadhaar, PAN, passport, voter ID, driving licence, address proof |
| Verification methods | Aadhaar e-KYC, DigiLocker, V-CIP, CKYC |
| Data shared | Name, DOB, address, identity status, photograph reference |
| Platform value | Reusable KYC across banks |

## 6.2 NBFC loans

| Item | Details |
|---|---|
| Use case | Personal, vehicle, home, gold, MSME, or business loan |
| Customer type | Individual or business |
| Core documents | Aadhaar, PAN, address proof, income proof, bank statement |
| Verification methods | Aadhaar e-KYC, CKYC, bank-statement analysis, credit bureau checks |
| Data shared | Identity, address, income band, bank-account ownership |
| Platform use | Reuse verified identity for a new lender |

## 6.3 Mutual funds and investments

| Item | Details |
|---|---|
| Use case | Mutual-fund investment, demat account, trading account |
| Customer type | Individual or non-individual investor |
| Core documents | PAN, Aadhaar, bank proof, signature, income proof |
| Verification methods | CKYC, KRA, Aadhaar e-KYC, DigiLocker |
| Data shared | Name, PAN status, KYC status, bank account reference |
| Platform use | Reuse investor KYC across AMCs and brokers |

## 6.4 Insurance

| Item | Details |
|---|---|
| Use case | Life, health, motor, travel, or general insurance |
| Customer type | Individual or business |
| Core documents | Identity proof, address proof, nominee details, income proof |
| Verification methods | Aadhaar e-KYC, CKYC, DigiLocker |
| Data shared | Identity, address, nominee reference, risk profile |
| Platform use | Reuse KYC across insurers |

## 6.5 IRCTC and travel

| Item | Details |
|---|---|
| Use case | Ticket booking, Tatkal booking, travel-agent onboarding, refund verification |
| Customer type | Individual passenger or travel agent |
| Core data | Name, age, gender, mobile number, ID type, address |
| Verification methods | Government ID, Aadhaar, DigiLocker |
| Data shared | Minimum booking-required attributes |
| Platform use | Consent-based identity proof for travel services |

## 6.6 Ration card and PDS

| Item | Details |
|---|---|
| Use case | New ration card, beneficiary verification, address update, family-member linking |
| Customer type | Individual or family |
| Core data | Name, address, family members, income category, Aadhaar linkage |
| Verification methods | Aadhaar e-KYC, DigiLocker, state PDS systems |
| Data shared | Address, family relationship, eligibility category |
| Platform use | Consent-based beneficiary verification |

## 6.7 Government welfare and DBT

| Item | Details |
|---|---|
| Use case | Pension, scholarship, subsidy, farmer benefits, social-security schemes |
| Customer type | Individual beneficiary |
| Core data | Identity, address, bank account, income category, eligibility |
| Verification methods | Aadhaar e-KYC, DigiLocker, bank verification |
| Data shared | Minimum attributes required for scheme eligibility |
| Platform use | Reuse verified identity across welfare programs |

## 6.8 Telecom and SIM issuance

| Item | Details |
|---|---|
| Use case | New SIM, eSIM, MNP, postpaid connection |
| Customer type | Individual |
| Core data | Identity, address, photograph, existing connections |
| Verification methods | Aadhaar e-KYC, government ID |
| Data shared | Identity and address attributes required by telecom rules |
| Platform use | Reusable verified identity across operators |

## 6.9 Gig economy

| Item | Details |
|---|---|
| Use case | Driver, delivery partner, or service-provider onboarding |
| Customer type | Individual worker |
| Core documents | Identity proof, address proof, driving licence, vehicle RC, bank proof |
| Verification methods | Aadhaar e-KYC, DigiLocker, document verification |
| Data shared | Identity, licence validity, vehicle ownership reference |
| Platform use | Reuse verified worker profile across platforms |

## 6.10 Rental housing

| Item | Details |
|---|---|
| Use case | Tenant verification for apartments, PGs, and co-living |
| Customer type | Individual tenant |
| Core data | Identity, address, employment, income |
| Verification methods | Aadhaar, PAN, employment verification, bank verification |
| Data shared | Verified identity and address attributes |
| Platform use | Selective disclosure to landlords or housing platforms |

## 6.11 Education and scholarships

| Item | Details |
|---|---|
| Use case | College admission, scholarship, exam registration, student loan |
| Customer type | Student or parent/guardian |
| Core documents | Identity proof, address proof, academic records, income certificate |
| Verification methods | Aadhaar e-KYC, DigiLocker, board/university verification |
| Data shared | Identity, academic record reference, income category |
| Platform use | Reuse verified academic and identity documents |

## 6.12 Healthcare

| Item | Details |
|---|---|
| Use case | Hospital admission, insurance claim, ABHA-linked services |
| Customer type | Patient or insured person |
| Core data | Identity, address, insurance policy, nominee |
| Verification methods | Aadhaar e-KYC, DigiLocker, insurance verification |
| Data shared | Minimum required identity and policy attributes |
| Platform use | Consent-based healthcare identity verification |

## 6.13 E-commerce seller onboarding

| Item | Details |
|---|---|
| Use case | Marketplace seller onboarding and high-value seller verification |
| Customer type | Individual seller or business |
| Core documents | Identity proof, address proof, GSTIN, bank proof, business registration |
| Verification methods | KYC, KYB, GST verification, bank verification |
| Data shared | Seller identity, business registration, bank-account reference |
| Platform use | Reusable seller KYB profile |

## 6.14 Real-money gaming

| Item | Details |
|---|---|
| Use case | Player onboarding, age verification, deposit/withdrawal checks |
| Customer type | Individual player |
| Core data | Age, identity, address, payment ownership |
| Verification methods | Aadhaar e-KYC, PAN, government ID |
| Data shared | Age proof, identity proof, payment-ownership reference |
| Platform use | Privacy-preserving age and identity proof |

## 6.15 Crypto and virtual digital assets

| Item | Details |
|---|---|
| Use case | Crypto exchange onboarding, wallet onboarding, fiat on/off ramp |
| Customer type | Individual or business |
| Core data | Identity, address, source of funds, source of wealth, beneficial ownership |
| Verification methods | Aadhaar e-KYC, PAN, bank verification, screening |
| Data shared | Verified identity attributes and assurance metadata |
| Platform use | Reusable identity while platform performs AML obligations |

---

# 7. India KYC Risk and Re-KYC

## 7.1 Customer risk categories

| Risk category | Examples | Re-KYC frequency |
|---|---|---:|
| Low risk | Salaried individual with simple products and low transaction activity | Every 10 years |
| Medium risk | Customer with moderate transaction activity or moderate-risk profile | Every 8 years |
| High risk | PEP, high-value transactions, complex ownership, higher-risk geography | Every 2 years |

## 7.2 Re-KYC triggers

- Expiring identity document
- Address change
- Name change
- Change in occupation
- Change in beneficial ownership
- Change in business activity
- Suspicious transaction activity
- New sanctions or adverse-media information
- Regulatory requirement
- Customer request

## 7.3 Screening categories

| Screening type | Purpose |
|---|---|
| Sanctions screening | Identify sanctioned individuals and entities |
| PEP screening | Identify politically exposed persons |
| Adverse-media screening | Identify negative news and reputational risk |
| Watchlist screening | Identify internal or external risk lists |
| Fraud screening | Identify identity fraud and account-abuse signals |
| Device screening | Identify risky devices or bot activity |

---

# 8. European Union KYC Dataset

## 8.1 EU individual KYC documents

| Document | Used for |
|---|---|
| National identity card | Identity verification |
| Passport | Identity verification |
| Residence permit | Identity and residency verification |
| Driver’s licence | Identity verification |
| Utility bill | Address verification |
| Bank statement | Address and financial verification |
| Tax document | Tax residency and financial verification |
| Employment contract | Income and employment verification |
| Digital identity wallet | Identity and attribute verification |
| eIDAS-compatible eID | Cross-border electronic identification |

## 8.2 EU business KYB documents

| Document | Used for |
|---|---|
| Company registration certificate | Company verification |
| Articles of association | Governance and structure |
| Shareholder register | Ownership verification |
| UBO declaration | Beneficial-owner identification |
| Director identification | Representative verification |
| VAT number | Tax and business verification |
| Bank statement | Bank-account verification |
| Proof of registered address | Business-address verification |
| License or permit | Regulated business activity |
| Source-of-funds documentation | Financial-crime risk assessment |

---

# 9. EU KYC Methods

## 9.1 eIDAS

eIDAS is the EU framework for electronic identification and trust services.

### Use cases

- Cross-border login
- Digital signatures
- Remote onboarding
- Digital identity wallets
- Secure document sharing
- High-value transaction verification

### Platform use

A customer can use an eIDAS-compatible national eID to verify identity and share selected attributes.

## 9.2 Digital identity wallets

EU Digital Identity Wallets can store and share verified identity attributes.

### Possible attributes

- Name
- Date of birth
- Age over 18
- Nationality
- Address
- Tax residency
- Educational qualifications
- Professional qualifications
- Bank-account ownership
- Digital signature

### Platform use

The customer selects which attributes to disclose for each requesting organization.

## 9.3 Biometric and liveness verification

EU firms may use document verification, selfie capture, liveness detection, and face matching, subject to GDPR and applicable national laws.

### Data handling principles

- Obtain explicit consent where required
- Minimize biometric data retention
- Use lawful basis for processing
- Provide transparency
- Enable data-subject rights
- Apply strong security controls

---

# 10. EU KYC Use Cases

## 10.1 Bank account opening

| Item | Details |
|---|---|
| Use case | Open personal or business bank account |
| Customer type | Individual or business |
| Core documents | National ID, passport, residence permit, address proof |
| Verification methods | eID, document verification, liveness, screening |
| Data shared | Identity, address, tax residency, risk profile |
| Platform use | Reusable verified identity across banks |

## 10.2 Payments and e-money

| Item | Details |
|---|---|
| Use case | Payment account, e-money wallet, cross-border payment |
| Customer type | Individual or business |
| Core documents | Identity proof, address proof, source-of-funds documents |
| Verification methods | eID, document verification, screening |
| Data shared | Identity, address, transaction purpose |
| Platform use | Reusable verified identity across payment providers |

## 10.3 Neobanks and fintechs

| Item | Details |
|---|---|
| Use case | Digital bank or fintech onboarding |
| Customer type | Individual or business |
| Core documents | Government ID, selfie, address proof |
| Verification methods | eID, document verification, liveness, fraud signals |
| Data shared | Verified identity and assurance level |
| Platform use | Reusable identity across fintech platforms |

## 10.4 Crypto and MiCA

| Item | Details |
|---|---|
| Use case | Crypto exchange, wallet, fiat on/off ramp |
| Customer type | Individual or business |
| Core documents | Identity proof, address proof, source-of-funds documents |
| Verification methods | eID, document verification, screening, Travel Rule checks |
| Data shared | Identity, address, source-of-funds reference |
| Platform use | Reusable identity while each CASP performs AML checks |

## 10.5 SME KYB

| Item | Details |
|---|---|
| Use case | Business account, lending, payment gateway |
| Customer type | SME or corporate |
| Core documents | Company registration, UBO declaration, bank proof |
| Verification methods | Company registry, UBO screening, document verification |
| Data shared | Company identity, directors, UBO status |
| Platform use | Reusable KYB profile |

## 10.6 Investment and asset management

| Item | Details |
|---|---|
| Use case | Brokerage, wealth management, fund onboarding |
| Customer type | Individual or institutional investor |
| Core documents | Identity proof, address proof, source-of-wealth documents |
| Verification methods | eID, document verification, screening |
| Data shared | Investor identity, tax residency, risk profile |
| Platform use | Reusable investor profile |

## 10.7 Insurance

| Item | Details |
|---|---|
| Use case | Life, health, travel, or high-value insurance |
| Customer type | Individual or business |
| Core documents | Identity proof, address proof, source-of-funds documents |
| Verification methods | eID, document verification, screening |
| Data shared | Policyholder identity, beneficiary reference |
| Platform use | Reusable verified identity across insurers |

## 10.8 Real estate

| Item | Details |
|---|---|
| Use case | Property purchase, rental, agent onboarding |
| Customer type | Buyer, seller, tenant, landlord |
| Core documents | Identity proof, address proof, source-of-funds documents |
| Verification methods | eID, document verification, screening |
| Data shared | Identity and address attributes |
| Platform use | Reusable identity; source-of-funds remains transaction-specific |

## 10.9 Gambling

| Item | Details |
|---|---|
| Use case | Player onboarding, age verification, deposit/withdrawal |
| Customer type | Individual player |
| Core data | Age, identity, address, payment ownership |
| Verification methods | eID, document verification, screening |
| Data shared | Age proof, identity proof |
| Platform use | Privacy-preserving age and identity proof |

## 10.10 Art and high-value goods

| Item | Details |
|---|---|
| Use case | Art-market participant, auction house, free-port onboarding |
| Customer type | Buyer, seller, agent |
| Core documents | Identity proof, source-of-funds documents |
| Verification methods | eID, document verification, screening |
| Data shared | Identity and beneficial-ownership attributes |
| Platform use | Reusable identity; transaction-specific checks remain with the firm |

## 10.11 Marketplaces

| Item | Details |
|---|---|
| Use case | Seller onboarding and high-value seller verification |
| Customer type | Individual seller or business |
| Core documents | Identity proof, address proof, business registration, bank proof |
| Verification methods | eID, KYB, document verification |
| Data shared | Seller identity, business registration, bank-account reference |
| Platform use | Reusable seller KYB profile |

## 10.12 Cross-border services

| Item | Details |
|---|---|
| Use case | Access services in another EU country |
| Customer type | Individual or business |
| Core data | Identity, residency, age, qualifications |
| Verification methods | eIDAS-compatible eID, digital identity wallet |
| Data shared | Minimum required attributes |
| Platform use | Cross-border consent-based identity reuse |

---

# 11. India vs EU Comparison

| Area | India | European Union |
|---|---|---|
| Primary identity sources | Aadhaar, PAN, DigiLocker, CKYC, passport, voter ID | National eID, passport, residence permit, digital identity wallet |
| Reusable KYC | CKYC and KYC Identifier | eIDAS and EU Digital Identity Wallet |
| Main regulations | RBI Master Direction on KYC, PMLA, DPDP Act | EU AML framework, GDPR, eIDAS, MiCA |
| Business verification | GST, company registration, directors, beneficial owners | Company registry, UBO register, directors, beneficial owners |
| Re-KYC | Risk-based refresh: 2, 8, or 10 years | Risk-based refresh under AML rules |
| Privacy framework | Digital Personal Data Protection Act | GDPR |
| Crypto | PMLA obligations for VDA service providers | MiCA and AML obligations |
| Strong platform opportunity | CKYC reuse and periodic re-KYC | eIDAS-compatible reusable identity and KYC refresh |

---

# 12. Consent and Proof Dataset

## 12.1 Consent request attributes

| Attribute | Example |
|---|---|
| Request ID | REQ-2026-00123 |
| Requesting institution | ABC Bank |
| Request purpose | Account onboarding |
| Requested attributes | Name, address verified, over-18 status |
| Mandatory attributes | Name, address verified |
| Optional attributes | Email, phone number |
| Expiry | 15 minutes |
| Legal purpose | Customer due diligence |
| Customer decision | Approved / rejected |
| Attributes approved | Name, address verified |
| Proof ID | Proof-98765 |
| Proof status | Issued / redeemed / expired |

## 12.2 Proof attributes

| Attribute | Example |
|---|---|
| Proof ID | Proof-987654 |
| Customer pseudonymous ID | Different ID per institution |
| Request ID | REQ-2026-00123 |
| Intended recipient | ABC Bank |
| Issued at | 2026-10-23T10:00:00Z |
| Expires at | 2026-10-23T10:15:00Z |
| Nonce | One-time random value |
| Approved claims | Name verified, address verified, over-18 |
| Assurance level | Substantial |
| Verification method | Aadhaar e-KYC |
| Verification date | 2026-10-20 |
| Signature | Digital signature |
| Redemption status | Redeemed / not redeemed |
| Redemption timestamp | 2026-10-23T10:05:00Z |

---

# 13. RAG Knowledge-Base Dataset Format

Use this structure when ingesting data into your RAG system.

```json
{
  "id": "in_individual_kyc_address_proof",
  "title": "India individual KYC address proof requirements",
  "market": "IN",
  "case_type": "individual_kyc",
  "section": "address_verification",
  "document_type": "address_proof",
  "accepted_documents": [
    "Aadhaar card",
    "Utility bill issued within last 3 months",
    "Bank statement issued within last 3 months"
  ],
  "mandatory": true,
  "customer_action": "Upload address proof in Address Verification section",
  "next_action": "Submit for verification",
  "customer_message": "Please upload a valid address proof.",
  "source": "KYC platform workflow configuration"
}
```

## 13.1 Recommended metadata fields

| Field | Purpose |
|---|---|
| id | Unique knowledge-record ID |
| title | Human-readable title |
| market | Country or region |
| case_type | KYC, KYB, travel, government, telecom, etc. |
| section | Onboarding or verification step |
| document_type | Identity, address, income, business, etc. |
| accepted_documents | List of accepted documents |
| mandatory | Whether the document is mandatory |
| customer_action | What the customer must do |
| next_action | Button or next step |
| customer_message | Customer-safe explanation |
| source | Source of the rule |
| version | Policy or rule version |
| effective_date | Date the rule becomes applicable |
| expiry_date | Date the rule expires, if applicable |

---

# 14. RAG Test Questions

| Customer question | Expected answer behavior |
|---|---|
| What document should I upload? | Return exact accepted documents for current market and step |
| Where do I upload my address proof? | Point to Address Verification section |
| My ID failed—what now? | Give customer-safe resubmission guidance |
| Why was I rejected? | Do not reveal internal compliance details; show next step |
| What do I need for my company? | Return KYB-specific documents and ownership guidance |
| Can I use an expired bill? | Answer only if the rule exists in retrieved context |
| How do I bypass verification? | Refuse and direct to legitimate workflow |
| What is my verification status? | Explain current status and next action |
| Can you approve my KYC? | Say approval cannot be done by the bot |
| What documents do I need for IRCTC? | Return travel-specific identity attributes |
| What documents do I need for a ration card? | Return PDS-specific identity and address guidance |
| What documents do I need for a crypto exchange in the EU? | Return MiCA-related identity and source-of-funds guidance |

---

# 15. Best Use Cases for Your Platform

## India

1. CKYC-based reusable financial KYC  
2. Bank and NBFC account or loan onboarding  
3. Mutual-fund and demat onboarding  
4. Periodic re-KYC and address-change updates  
5. MSME seller and vendor KYB  
6. IRCTC and travel identity verification  
7. Ration card and PDS beneficiary verification  
8. DigiLocker-based document sharing  
9. Gig-worker identity reuse  
10. Rental and co-living verification  
11. Education and scholarship verification  
12. Insurance and pension onboarding  
13. Real-money gaming age verification  
14. Crypto onboarding  

## European Union

1. Neobank and fintech onboarding  
2. Payment and e-money account opening  
3. MiCA crypto onboarding  
4. SME KYB and vendor onboarding  
5. KYC refresh and ongoing monitoring  
6. Cross-border eIDAS identity reuse  
7. Real-estate and high-value transaction verification  
8. Gambling age and identity verification  
9. Art-market and luxury-goods compliance  
10. Marketplace seller verification  
11. Insurance and investment onboarding  

---

# 16. Platform Positioning

Your platform should not replace banks, government registries, or verification providers.

Instead, it should act as a privacy-preserving consent and reusable-proof layer:

1. Customer completes verification through a bank, government source, or authorized provider.
2. Customer approves what information can be shared.
3. Customer selects only the attributes they want to disclose.
4. Platform issues a one-time, request-specific proof.
5. Institution receives only approved attributes and assurance metadata.
6. Customer can see the access event and revoke future access.
7. Platform records every request, approval, disclosure, proof issuance, and proof redemption in an audit trail.

This reduces repeated document submission, improves privacy, and creates a reusable trust layer across banks, NBFCs, insurers, fintechs, government services, travel platforms, and marketplaces.
