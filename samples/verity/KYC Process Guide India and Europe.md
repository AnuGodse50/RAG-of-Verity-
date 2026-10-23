KYC Process Guide: India and Europe 

# KYC Process Guide: India and Europe 

Team CodeVerse · Prepared 20 October 2026 

**What this is:** a plain-English walk-through of how KYC (Know Your Customer) works today in India and in Europe: who must do it, where it is required, how it is done step by step, which documents are needed, where the data is stored, and how long it is kept. India and Europe are kept in separate parts, followed by a side-by-side comparison. 

**Please note:** this is a planning guide, not legal advice. Amounts, intervals and section numbers marked "verify" should be checked against the RBI Master Direction, the PML Rules, and EU texts (EUR-Lex) before you rely on them. The EU is changing: most of today's rules are national, and a single EU rulebook starts on 10 July 2027. 

## Words used in this guide 

- **KYC:** checking who a customer is before and during a business relationship. 

- **CDD (Customer Due Diligence):** the full set of KYC checks: identify, verify, understand the purpose of the relationship, find beneficial owners, and monitor. 

- **Beneficial owner:** the real person who ultimately owns or controls a company or trust. **PEP (Politically Exposed Person):** a person with a prominent public role, treated as higher risk. 

- **EDD / SDD:** Enhanced Due Diligence (stricter checks for high risk) and Simplified Due Diligence (lighter checks for low risk). 

- **Regulated Entity (India) / Obliged Entity (EU):** a business the law requires to do KYC. 

- **STR:** Suspicious Transaction Report sent to the financial intelligence unit. 

# Part 1. India 

## 1.1 Who rules KYC in India 

|Body|Role|
|---|---|
|Parliament (PMLA 2002) and the PML|The legal base: customer identification,|
|Rules 2005|record keeping, reporting.|



Page 1 of 14 

KYC Process Guide: India and Europe 

|Body|Role|
|---|---|
|RBI|KYC Master Direction for banks, NBFCs,<br>payment entities and other RBI-regulated<br>firms.|
|SEBI|KYC for brokers, mutual funds and other<br>market intermediaries, via KYC Registration<br>Agencies (KRAs).|
|IRDAI|KYC/AML for insurers and intermediaries.|
|PFRDA|KYC for pension subscribers (NPS).|
|FIU-IND|Receives suspicious and cash transaction<br>reports.|
|CERSAI|Runs the Central KYC Records Registry<br>(CKYCR).|
|UIDAI|Runs Aadhaar and its authentication and<br>offline verification systems.|



## 1.2 Where KYC is required in India 

#### **Financial sector (law requires full KYC):** 

- Commercial, small finance, payments and cooperative banks, regional rural banks. 

- NBFCs, housing finance companies, asset reconstruction companies. 

- Prepaid payment instrument (wallet) issuers, with different levels (minimum-KYC and full-KYC). 

- Payment aggregators and money transfer / forex dealers. 

- Securities: stock brokers, depository participants, mutual funds, portfolio managers. Insurance: insurers, brokers and agents (KYC at policy issue and at claim or payout in many cases). 

- Pensions: NPS points of presence and central record keepers. 

- Designated non-financial businesses under PMLA, for example casinos, dealers in precious metals and stones, real estate dealers, and certain professionals such as chartered accountants and company secretaries for specified activities (verify the current notified list). 

Page 2 of 14 

KYC Process Guide: India and Europe 

#### Virtual digital asset service providers (since 2023). 

**Everyday situations where an ID check is asked, though it is not always full AML KYC:** 

- New SIM cards (telecom rules, often Aadhaar e-KYC or documents). 

- Hotel check-in (ID photocopy by practice; foreign guests also have a separate registration form). 

Gig platforms, employers and background checks. 

Loan and credit card applications, demat account opening, GST and tax registrations. 

1.3 The KYC process, step by step (banks and other RBI-regulated entities) 

1. **Customer Acceptance Policy.** The institution decides who it will and will not serve. Anonymous and fictitious accounts are not allowed. 

2. **Customer Identification Procedure (CIP).** The person gives identity details and documents. The institution identifies and verifies them. 

3. **Customer Due Diligence (CDD).** For an individual: verify identity and address with approved documents, collect PAN (or Form 60), a photograph, and understand the purpose of the account. For companies and others: also identify the entity and its beneficial owners. 

4. **Risk categorisation.** Each customer is rated low, medium or high risk based on type, occupation, geography and product. 

5. **Screening.** Check names against sanctions and terror lists, and against PEP lists. 

6. **Enhanced due diligence** for high-risk customers, such as source of funds and seniormanagement approval for PEPs. 

7. **Account opening.** The institution assigns a customer ID (often a unified customer ID across products). 

8. **CKYC upload.** The institution uploads the KYC record to the Central KYC Registry, which issues a KYC Identifier (KIN). The upload is due soon after account opening; the RBI prescribes the deadline (verify, recently stated as 10 days). 

9. **Ongoing monitoring.** Watch transactions for consistency with the customer's profile. 

10. **Periodic updation.** Refresh KYC on a cycle based on risk: at least every **2 years for high risk, 8 years for medium risk, and 10 years for low risk** . Recent amendments simplified the process (for example, customers with no change can confirm by self-declaration). 

Page 3 of 14 

KYC Process Guide: India and Europe 

11. **Reporting.** File Suspicious Transaction Reports (within days of concluding a transaction is suspicious, verify the exact period) and cash and other threshold reports with FIU-IND. 

12. **Closure and retention.** Keep records for at least five years after the relationship ends (see 1.6). 

## 1.4 The ways KYC can be done 

|Method|How it works|Notes|
|---|---|---|
|In person with documents|Customer brings an<br>Officially Valid Document<br>(OVD). The institution<br>verifies the original or a<br>certified copy.|Traditional branch route.|
|Aadhaar offline verification<br>(Paperless Offline e-KYC)|Customer generates a<br>signed XML file from UIDAI<br>and shares it with a self-<br>chosen share code. The<br>institution verifies the<br>signature offline.|No live call to UIDAI. The<br>Aadhaar number must not be<br>stored in full or shared<br>onward.|
|Aadhaar e-KYC by OTP|Customer enters an OTP<br>sent to their Aadhaar-linked<br>mobile.|Usually limited accounts,<br>later converted to full KYC<br>within a time limit.|
|Aadhaar biometric e-KYC|Fingerprint or iris<br>authentication.|Only for entities permitted<br>by law (such as banks).|
|DigiLocker|Customer authorises the<br>institution to fetch<br>government-issued e-<br>documents.|Treated as an equivalent e-<br>document of an OVD.<br>Business access needs<br>onboarding through API<br>Setu.|
|CKYC retrieval|Institution fetches an<br>existing KYC record using<br>the customer's KYC<br>Identifier, with the<br>customer's authorisation.|Avoids repeating full KYC,<br>but the institution must still<br>be satisfied (and update<br>records if details changed).|



Page 4 of 14 

KYC Process Guide: India and Europe 

|Method|How it works|Notes|
|---|---|---|
|Digital KYC (app based)|An authorised official<br>captures a live photograph<br>of the customer and the<br>document at a geo-tagged<br>location.|Done on the institution's<br>controlled application.|
|Video-based CIP (V-CIP)|A live video session with an<br>official of the institution,<br>with recording, photograph<br>capture, liveness check,<br>face match to the OVD, and<br>random questions.|Allowed for new accounts,<br>converting limited accounts<br>to full KYC, and periodic<br>updation. Must be done on<br>secure institution-controlled<br>infrastructure.|
|Business correspondents|Field agents assist<br>customers, mostly for<br>financial inclusion.|Recent amendments<br>formalised KYC through<br>business correspondents.|
|Reliance on a third party|The institution relies on<br>another regulated entity's<br>CDD, getting the records<br>immediately.|The relying institution stays<br>responsible.|



## 1.5 Documents needed in India 

### Individuals 

- **Officially Valid Documents (OVD):** passport, driving licence, proof of possession of Aadhaar number, voter ID card, NREGA job card, and the letter issued by the National Population Register. The OVD must show current address, or the customer provides a "deemed OVD" for address (for example a recent utility bill, property tax receipt or pension order; verify the current list and age limits). 

- **PAN** (Permanent Account Number) or **Form 60** if the customer has no PAN. **Recent photograph.** 

- **Other items depending on product:** income proof, source of funds for high-risk, occupation details, mobile number for authentication. 

Page 5 of 14 

KYC Process Guide: India and Europe 

### Simplified options for low-risk customers 

- **Small accounts** for people without OVDs, with a self-attested photo and signature before an official, and strict limits on balance, yearly credits and monthly withdrawals (verify the limits, which were about ₹50,000 balance, ₹1 lakh yearly credit and ₹10,000 monthly withdrawal, valid for a limited period). 

- **Aadhaar OTP accounts** with balance and period limits, converted to full KYC later. **Minimum-KYC wallets** with lower limits. 

### Companies, firms and others 

- **Company:** certificate of incorporation, memorandum and articles, PAN, board resolution authorising signatories, OVDs of officers and signatories, and identification of **beneficial owners** (generally anyone with a controlling ownership interest above a stated percentage, such as 10% for companies; verify thresholds under the PML Rules). 

- **Partnership firm:** registration certificate, partnership deed, PAN, and OVDs of partners and signatories (beneficial owner threshold is generally higher, such as 15%; verify). 

- **Trust:** registration certificate, trust deed, PAN, and identification of trustees, settlors, beneficiaries and anyone with control. 

- **Sole proprietorship:** KYC of the proprietor plus business proof (registration, GST, licence or similar). 

- **Unincorporated bodies:** resolution of the managing body and identification documents of those acting. 

### Extra for high-risk 

Source of funds and wealth, senior-management approval (PEPs), and more frequent updates. 

Page 6 of 14 

KYC Process Guide: India and Europe 

## 1.6 Where the data is stored and for how long 

|Place|What is stored|Who controls it|
|---|---|---|
|The institution's own<br>systems (core banking and<br>KYC system)|Full KYC file: identity<br>documents, address proof,<br>photos, risk rating, screening<br>results, account details.|The regulated entity.|
|Central KYC Records<br>Registry (CKYCR), run by<br>CERSAI|A standard KYC record<br>(identity and address details<br>plus images of documents)<br>tied to a KYC Identifier.|CERSAI, fed by regulated<br>entities.|
|KYC Registration Agencies<br>(securities)|KYC records for market<br>intermediaries, shared across<br>SEBI-registered firms.|SEBI-registered KRAs.|
|Aadhaar Data Vault|Where entities permitted to<br>hold Aadhaar numbers must<br>keep them in a vault, with<br>reference keys used<br>elsewhere.|The entity, under UIDAI<br>rules.|
|V-CIP recordings|Audio-video and photograph<br>of the session, kept with<br>tamper evidence and<br>timestamps.|The institution, in India.|
|DigiLocker|The citizen's own issued<br>documents. Institutions get a<br>copy only with consent.|Government (NeGD).|
|Transaction and log systems|Transaction records and<br>system logs.|The institution. CERT-In<br>expects logs kept in India<br>for a rolling 180 days.|



**How long:** PMLA and the PML Rules require identity records and transaction records to be kept for at least **five years** after the relationship ends or the transaction takes place (verify the wording for each record type). Your Costing report mentions 10-year retention for V-CIP video. I could not confirm that figure, so check the RBI direction before using it. 

Page 7 of 14 

KYC Process Guide: India and Europe 

**Where:** the data stays within the regulated entity's control, and RBI payment-data and CERT-In rules push key data and logs into India. Cross-border transfers are separately restricted by DPDP and by sector rules. 

## 1.7 What KYCVault can and cannot do in India 

- **Can:** help a regulated entity collect KYC with consent, give the customer a reusable credential, show the audit trail, and cut repeat checks by retrieving through proper channels. 

- **Cannot:** replace CKYCR, replace V-CIP, or let one bank skip its own responsibility. The receiving regulated entity must still decide risk, monitor, update and report. 

# Part 2. Europe (EU) 

## 2.1 How KYC works in the EU today and from July 2027 

Today, KYC in the EU is based on the Anti-Money Laundering Directives (mainly Directive 2015/849 as amended), which each member state turned into its own national law, plus European Banking Authority (EBA) guidelines on risk factors and remote onboarding. This means detail differs by country. 

From **10 July 2027** , the **AML Regulation (AMLR, Regulation 2024/1624)** applies directly in all member states as one customer due diligence rulebook. Technical standards from the new **AML Authority (AMLA)** fill in detail, including how electronic identification can be used. AMLA is also preparing direct supervision of the highest-risk firms from 2028. 

There is **no single central KYC registry** in the EU comparable to India's CKYCR. Each obliged entity keeps its own file, though some countries have national eID schemes (for example Nordic bank-based IDs and Belgium's itsme) or private utilities that banks use. 

## 2.2 Where KYC is required in the EU 

**Obliged entities under the AML rules include:** 

- Credit institutions (banks) and financial institutions. 

- Payment institutions and electronic money institutions. Investment firms, fund managers and other securities businesses. Insurers (life insurance) and insurance intermediaries. 

Page 8 of 14 

KYC Process Guide: India and Europe 

- Crypto-asset service providers (CASPs). 

- Consumer credit and mortgage lenders and intermediaries, crowdfunding platforms. Auditors, external accountants and tax advisers. 

- Notaries and lawyers (when handling specified transactions). 

- Real estate agents. 

- Trust and company service providers. 

- Dealers in high-value goods and precious metals. 

- Casinos and gambling service providers. 

- Under the AMLR, certain professional football clubs and agents. 

#### **Other situations that involve identity checks but are national or sector specific:** 

- SIM card registration (rules vary by country). 

- Hotel guest registration (required in several member states). 

- Online age verification for restricted services. 

- Employer right-to-work checks. 

## 2.3 When due diligence is triggered 

- When starting a **new business relationship** . 

- For **occasional transactions of €10,000 or more** , whether in one go or linked. 

- When there is a **suspicion** of money laundering or terrorist financing. 

- When there are **doubts** about earlier identification data. 

- On **trigger events** during the relationship (a change in ownership, behaviour or risk). 

## 2.4 The KYC process, step by step 

1. **Firm-wide risk assessment.** The obliged entity first assesses its own moneylaundering risks (customers, products, countries, delivery channels). 

2. **Identify the customer.** Collect identity details (see 2.6). 

3. **Verify** with reliable and independent sources: documents, data, or electronic identification. 

4. **Identify the beneficial owner** of companies and trusts, and take reasonable steps to verify them, including checks against the national beneficial ownership register (generally 25% ownership or control, with lower thresholds in some high-risk cases; verify). 

Page 9 of 14 

KYC Process Guide: India and Europe 

5. **Understand the purpose and nature** of the relationship, and the expected activity. 

6. **Screen** against sanctions lists and for PEPs, and check adverse media where risk requires. 

7. **Assign a risk level** and apply **simplified** , **standard** or **enhanced** due diligence. Enhanced checks include source of funds and wealth and senior-management approval. 

8. **Open the relationship** only after verification (limited exceptions exist). 

9. **Monitor** transactions and the relationship continuously. 

10. **Update customer information** regularly: at least **once a year for higher-risk customers and every five years for others** , plus when a trigger event happens. 

11. **Report** suspicious activity to the national Financial Intelligence Unit (FIU), without tipping off the customer. 

12. **Keep records** for five years, then delete (see 2.7). 

## 2.5 The ways KYC can be done 

|Method|How it works|Notes|
|---|---|---|
|In person with documents|Staff see the original ID and<br>check it.|Still accepted.|
|Electronic identification<br>(eID)|Customer authenticates with<br>a national eID scheme at the<br>right assurance level<br>("substantial" or "high" under<br>eIDAS).|The preferred remote route<br>under AMLR and draft AMLA<br>standards.|
|Qualified trust services|For example a qualified<br>electronic signature or<br>attestation.|Also recognised as a strong<br>remote method.|
|**EU Digital Identity Wallet**<br>**(EUDI Wallet)**|Customer shares verified<br>attributes from the wallet<br>(Person Identification Data,<br>plus attestations).|Member states must offer<br>wallets by late December<br>2026. Obliged entities such<br>as banks must accept them<br>by December 2027.|



Page 10 of 14 

KYC Process Guide: India and Europe 

|Method|How it works|Notes|
|---|---|---|
|Remote document-based<br>onboarding|Customer photographs the ID<br>document and takes a selfie<br>or video. The system checks<br>image quality, document<br>validity, liveness and face<br>match.|A fallback when eID is<br>unavailable or cannot<br>reasonably be provided.<br>Draft technical standards<br>require safeguards and<br>secure, time-stamped copies<br>of the verified documents.|
|Video identification|A live video call with a trained<br>agent.|Accepted in several<br>countries (Germany is well<br>known for it), subject to<br>national rules.|
|NFC chip reading|The phone reads the chip in a<br>passport or ID card.|Strengthens remote<br>document checks.|
|Reliance on, or<br>outsourcing to, a third<br>party|Another obliged entity or a<br>provider performs CDD.|The obliged entity stays<br>responsible for compliance.|



## 2.6 Documents and data needed in the EU 

### Individuals 

- **Data collected:** full names, date of birth, place of birth in many countries, nationality, residential address, and a national or tax ID number where available (verify the exact list in AMLR Article 22 and national law). 

- **Documents:** valid passport, national ID card, or residence permit. A proof of address (such as a utility bill or bank statement) is asked when the address cannot be confirmed from the ID or other reliable data. 

- **For higher risk:** source of funds and source of wealth evidence, such as payslips, tax returns, sale contracts or account statements. 

### Companies and other entities 

- Extract from the company registry or equivalent proof of existence. 

- Articles of association and a document showing who may represent the company. Identity of directors and authorised signatories. 

Page 11 of 14 

KYC Process Guide: India and Europe 

Ownership structure and identification of **beneficial owners** , checked against the national beneficial ownership register. 

- For trusts: trust deed or extract, and identification of settlor, trustees, protectors, beneficiaries and anyone with control. 

## 2.7 Where the data is stored and for how long 

|Place|What is stored|Who controls it|
|---|---|---|
|The obliged entity's own<br>systems|The CDD file: copies of<br>identity documents and data,<br>verification results, risk<br>assessment, screening<br>results, transaction records,<br>monitoring and reports.|The obliged entity (a data<br>controller under GDPR).|
|Outsourced providers|The same data, held on the<br>entity's behalf.|The provider as processor,<br>under a contract. The entity<br>stays responsible.|
|National beneficial<br>ownership registers|Ownership data about<br>companies and trusts.|National authorities.|
|FIU systems|Suspicious activity reports.|National FIUs.|
|The customer's EUDI<br>Wallet (on their device)|Their own identity and<br>attestations.|The customer.|
|Cloud and hosting|Must meet GDPR rules on<br>transfers if outside the EU or<br>EEA.|The entity, with processor<br>contracts.|



**How long:** records must be kept for **five years after the end of the business relationship** or the date of an occasional transaction. Records must be kept unredacted, and personal data must be **deleted when the period ends** , unless other EU or national law requires otherwise. Authorities can ask for a further period, capped at five more years in defined cases. An obliged entity may keep references instead of copies if the reference lets it give authorities the information immediately and the information cannot be changed. 

Page 12 of 14 

KYC Process Guide: India and Europe 

## 2.8 How the process differs by country (until July 2027) 

Until the AMLR applies, national law decides many details: accepted ID documents, whether video identification is allowed, deadlines for verification, and the use of national eID schemes. When you choose a first EU country, map its national rules, the supervisor, the FIU, and the available eID schemes. 

## 2.9 What KYCVault can and cannot do in the EU 

- **Can:** help obliged entities collect and share KYC data in a minimum-disclosure way, carry credentials that fit EUDI Wallet formats, and keep a consent and audit record. 

- **Cannot:** replace the obliged entity's own risk assessment, monitoring and reporting duties, or be treated as an approved eID means unless it is recognised under the eIDAS framework. 

# Part 3. India and EU side by side 

|Topic|India|EU|
|---|---|---|
|Main law|PMLA 2002, PML Rules 2005,<br>RBI and sector directions|AMLR (from 10 Jul 2027), AMLA<br>standards, national laws until<br>then|
|Who sets detail|RBI, SEBI, IRDAI, PFRDA|AMLA, EBA, national<br>supervisors|
|Central KYC registry|Yes (CKYCR)|No EU-wide registry|
|Digital identity base|Aadhaar offline XML,<br>DigiLocker, CKYC|eID schemes, EUDI Wallet|
|Video-based KYC|V-CIP, with detailed rules|Video identification accepted in<br>some countries, with standards<br>for remote onboarding|
|Periodic refresh|2, 8 or 10 years by risk|At least yearly for high risk, 5<br>years for others|
|Record retention|About 5 years after<br>relationship ends|5 years after relationship ends,<br>then delete|



Page 13 of 14 

KYC Process Guide: India and Europe 

|Topic|India|EU|
|---|---|---|
|Occasional<br>transaction threshold|Set in rules and by sector|€10,000|
|Beneficial owner<br>thresholds|About 10% for companies and<br>15% for firms (verify)|Generally 25%, lower for some<br>high-risk cases (verify)|
|Where data lives|In India for key data and logs, in<br>the regulated entity's control|In the obliged entity's control,<br>with GDPR limits on transfers|
|Privacy law alongside|DPDP Act and Rules|GDPR|
|Reliance on others|Allowed, relying entity stays<br>responsible|Allowed, obliged entity stays<br>responsible|



# Part 4. What the product should capture for each KYC event 

To work in both regions, record at least: 

1. Who did the KYC (the regulated or obliged entity) and under which law. 

2. The method used (document, Aadhaar offline, DigiLocker, eID, EUDI Wallet, V-CIP, video identification). 

3. The assurance level and evidence references (without copying raw documents where possible). 

4. The date verified, risk category, and the **next update due date** . 

5. The attributes verified, and which ones were shared with whom, for what purpose, and until when. 

6. The retention clock and any legal hold. 

7. Revocation or status and the reason. 

8. Where the record is stored (region and system). 

**Sources to verify before relying on anything above:** RBI Master Direction on KYC (with 2025 amendments), PMLA and PML Rules, SEBI, IRDAI and PFRDA circulars, CERSAI CKYCR operating guidelines, UIDAI regulations, EUR-Lex text of Regulation (EU) 2024/1624 (especially Articles 22 and 77), AMLA draft technical standards on customer due diligence, and EBA guidelines. Commentary from vendors and law firms is useful for planning but is not a substitute for the official text. 

Page 14 of 14 

