# Fact check

28 claims across 9 posts. Each claim is written out in plain words, then tied to verbatim quotes from the sources. `python3 scripts/verify.py` confirms every quote is present in the saved source text (and, with `--live`, on the live page today).

Status key: Captured automatically means a screenshot with the quote highlighted is in `evidence/captures/`. Manual screenshot pending means the text is verified but the page could not be captured automatically; see `evidence/manual/README.md`.

## Post 1

```text
Redbelly, explained without the jargon.

It is a public network, built in Australia, where real financial assets like bonds, investment funds and loans can be issued, managed and traded as digital items. With ID checks and the rules built in.

Here is why that matters. 1/9
```

### C01. Redbelly is a public network.

- `S10-Q1` from S10 PDF p.15 (printed p.12), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Pilot use cases were conducted on a range of public and private [...] platforms, including Canvas Connect (private), Ethereum (public), Hedera (both public and private instances), Redbelly Network (public)"
  - Captured automatically: `evidence/captures/S10-Q1.png`
- `S07-Q1` from S07, Tokeniser Pty Ltd: "Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure, with identity and eligibility built into the protocol."
  - Captured automatically: `evidence/captures/S07-Q1.png`
- `S12-Q2` from S12, Redbelly Network: "Redbelly is Digital Public Token Infrastructure"
  - Captured automatically: `evidence/captures/S12-Q2.png`

### C02. Redbelly was built in Australia.

- `S03-Q5` from S03, Redbelly Network: "Redbelly Network, which was developed at the University of Sydney and CSIRO"
  - Captured automatically: `evidence/captures/S03-Q5.png`
- `S11-Q3` from S11, Redbelly Network: "with the support of the University of Sydney, CSIRO's Data 61, and Block8"
  - Captured automatically: `evidence/captures/S11-Q3.png`
- `S02-Q1` from S02, Redbelly Network: "2021 June Block8, CSIRO and University of Sydney create Redbelly Network as a joint venture with seed funding"
  - Manual screenshot pending: `evidence/manual/S02-Q1.png`

### C03. Financial assets such as bonds, investment funds and loans can be issued, managed and traded on it.

- `S01-Q1` from S01, Redbelly Network: "Redbelly provides the infrastructure to issue, manage, and distribute regulated digital financial assets to a global investor base."
  - Captured automatically: `evidence/captures/S01-Q1.png`
- `S01-Q3` from S01, Redbelly Network: "Treasuries & Bonds [...] Private Credit [...] Real Estate"
  - Captured automatically: `evidence/captures/S01-Q3.png`
- `S10-Q5` from S10 PDF p.60 (printed p.57), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Australian Bond Exchange piloted secondary market transactions involving the purchase of a tokenised corporate bond digital twin [...] using wCBDC as the settlement asset. Both the tokenised bond and the wCBDC were issued on to the same network. [...] network used in use case: Redbelly Network."
  - Captured automatically: `evidence/captures/S10-Q5.png`
- `S10-Q6` from S10 PDF p.63 (printed p.60), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Macropod piloted two use cases. The first use case tested issuance, trading and redemption of tokenised units in a [...] wholesale managed investment scheme, with registration and [...] distribution handled through the Tokeniser platform."
  - Captured automatically: `evidence/captures/S10-Q6.png`
- `S10-Q8` from S10 PDF p.64 (printed p.61), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "NotCentralised piloted the structuring, issuance and management of a tokenised structured finance security backed by loans. [...] network used in use case: Redbelly Network."
  - Captured automatically: `evidence/captures/S10-Q8.png`
- `S12-Q1` from S12, Redbelly Network: "Redbelly is designed to meet the requirements of regulated financial markets, providing open infrastructure that enables institutions to issue, manage, and distribute digital financial assets at scale."
  - Captured automatically: `evidence/captures/S12-Q1.png`

### C04. ID checks and the asset's rules are built in.

- `S07-Q1` from S07, Tokeniser Pty Ltd: "Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure, with identity and eligibility built into the protocol."
  - Captured automatically: `evidence/captures/S07-Q1.png`
- `S01-Q2` from S01, Redbelly Network: "A network of clean liquidity and verified participants enables structured products with clearly defined investor eligibility."
  - Captured automatically: `evidence/captures/S01-Q2.png`
- `S12-Q4` from S12, Redbelly Network: "A network of clean liquidity, combined with verifiable credentials enable tokenised investment products with defined investor eligibility, enforced at the point of trade."
  - Captured automatically: `evidence/captures/S12-Q4.png`

## Post 2

```text
Start with the problem. Buying into a bond or a fund today means money and paperwork passing between several companies. Each one keeps its own records, and they all have to be matched up, sometimes by hand. That costs time and money. 2/9
```

### C05. In traditional finance, several institutions keep separate records that must be reconciled, which can need manual work and costs money.

- `S10-Q4` from S10 PDF p.29 (printed p.26), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "In traditional financial systems, composability is usually achieved by using workflows to coordinate actions provided by different institutions and systems. The workflows are often complex and can require expensive manual coordination, reconciliation, and corrective steps"
  - Captured automatically: `evidence/captures/S10-Q4.png`

## Post 3

```text
Now picture a digital concert ticket. It proves the seat is yours, it moves to a new owner in seconds, and the venue sets the rules on who can resell it.

Redbelly lets financial assets work the same way. In finance, this is called tokenisation. 3/9
```

### C06. Tokenisation records ownership of a financial asset as a digital item and lets the issuer program the asset's rules.

- `S07-Q4` from S07, Tokeniser Pty Ltd: "Tokenisation records ownership of financial products and services as digital tokens, and lets you program the rules of the asset."
  - Captured automatically: `evidence/captures/S07-Q4.png`

### C07. Redbelly is infrastructure for issuing and moving these digital financial assets.

- `S01-Q1` from S01, Redbelly Network: "Redbelly provides the infrastructure to issue, manage, and distribute regulated digital financial assets to a global investor base."
  - Captured automatically: `evidence/captures/S01-Q1.png`
- `S07-Q1` from S07, Tokeniser Pty Ltd: "Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure, with identity and eligibility built into the protocol."
  - Captured automatically: `evidence/captures/S07-Q1.png`
- `S12-Q1` from S12, Redbelly Network: "Redbelly is designed to meet the requirements of regulated financial markets, providing open infrastructure that enables institutions to issue, manage, and distribute digital financial assets at scale."
  - Captured automatically: `evidence/captures/S12-Q1.png`

## Post 4

```text
The part most people miss: Redbelly is designed so the people using it are verified. Each transfer can be checked against the asset's rules automatically. And privacy tech is used so that being verified does not mean showing everyone your personal details. 4/9
```

### C08. Redbelly is designed so that participants are known and verified.

- `S06-Q1` from S06, Redbelly Network: "an innovative identity layer that ensures all network participants are known."
  - Captured automatically: `evidence/captures/S06-Q1.png`
- `S01-Q2` from S01, Redbelly Network: "A network of clean liquidity and verified participants enables structured products with clearly defined investor eligibility."
  - Captured automatically: `evidence/captures/S01-Q2.png`
- `S03-Q4` from S03, Redbelly Network: "Participants verify their identities, but their privacy remains protected through zero-knowledge proofs."
  - Captured automatically: `evidence/captures/S03-Q4.png`
- `S12-Q3` from S12, Redbelly Network: "Verified participants enable full auditability and clear accountability across all transactions"
  - Captured automatically: `evidence/captures/S12-Q3.png`

### C09. Transfers can be checked against the asset's rules automatically.

- `S07-Q3` from S07, Tokeniser Pty Ltd: "Every holder is verified and every transfer checked against the asset's rules, automatically."
  - Captured automatically: `evidence/captures/S07-Q3.png`
- `S07-Q1` from S07, Tokeniser Pty Ltd: "Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure, with identity and eligibility built into the protocol."
  - Captured automatically: `evidence/captures/S07-Q1.png`
- `S12-Q5` from S12, Redbelly Network: "Eligibility can be verified programmatically at the point of issuance and trade"
  - Captured automatically: `evidence/captures/S12-Q5.png`
- `S12-Q4` from S12, Redbelly Network: "A network of clean liquidity, combined with verifiable credentials enable tokenised investment products with defined investor eligibility, enforced at the point of trade."
  - Captured automatically: `evidence/captures/S12-Q4.png`

### C10. Privacy technology (zero-knowledge proofs) protects participants' privacy while they are verified.

- `S03-Q4` from S03, Redbelly Network: "Participants verify their identities, but their privacy remains protected through zero-knowledge proofs."
  - Captured automatically: `evidence/captures/S03-Q4.png`

## Post 5

```text
So who keeps the records straight? No single computer gets the final say. A group of computers must agree on every transaction, using a voting method developed at the University of Sydney. Once something is confirmed, it is final, and everyone sees the same version. 5/9
```

### C11. No single computer controls the outcome; agreement is reached through a democratic process.

- `S03-Q2` from S03, Redbelly Network: "DBFT achieves consensus through a democratic process where no single node controls the outcome."
  - Captured automatically: `evidence/captures/S03-Q2.png`

### C12. The agreement method (DBFT) was developed at the University of Sydney.

- `S03-Q1` from S03, Redbelly Network: "Democratic Byzantine Fault Tolerant (DBFT) consensus mechanism, developed and rigorously tested at the University of Sydney."
  - Captured automatically: `evidence/captures/S03-Q1.png`

### C13. Confirmed transactions are final and there is one consistent record, with no forking.

- `S03-Q3` from S03, Redbelly Network: "This means Redbelly maintains a single, consistent transaction record with no forking or branching"
  - Captured automatically: `evidence/captures/S03-Q3.png`
- `S06-Q2` from S06, Redbelly Network: "guarantee the impossibility of forking and mitigate double spending with near-instant finality."
  - Captured automatically: `evidence/captures/S06-Q2.png`
- `S12-Q6` from S12, Redbelly Network: "Deterministic finality ensures transactions are confirmed once and cannot be reversed"
  - Captured automatically: `evidence/captures/S12-Q6.png`

## Post 6

```text
Where it comes from: Redbelly grew out of research at the University of Sydney and CSIRO, Australia's national science agency. The live network launched in November 2024. Tokeniser, a Redbelly Network project, runs on it for Australian funds and companies. 6/9
```

### C14. Redbelly came out of research at the University of Sydney and CSIRO.

- `S03-Q5` from S03, Redbelly Network: "Redbelly Network, which was developed at the University of Sydney and CSIRO"
  - Captured automatically: `evidence/captures/S03-Q5.png`
- `S07-Q2` from S07, Tokeniser Pty Ltd: "Tokeniser is a Redbelly Network project: [...] born from research at the University of Sydney and Australian Government Science Agency: CSIRO"
  - Captured automatically: `evidence/captures/S07-Q2.png`
- `S11-Q3` from S11, Redbelly Network: "with the support of the University of Sydney, CSIRO's Data 61, and Block8"
  - Captured automatically: `evidence/captures/S11-Q3.png`
- `S02-Q1` from S02, Redbelly Network: "2021 June Block8, CSIRO and University of Sydney create Redbelly Network as a joint venture with seed funding"
  - Manual screenshot pending: `evidence/manual/S02-Q1.png`

### C15. CSIRO is Australia's national science agency.

- `S07-Q2` from S07, Tokeniser Pty Ltd: "Tokeniser is a Redbelly Network project: [...] born from research at the University of Sydney and Australian Government Science Agency: CSIRO"
  - Captured automatically: `evidence/captures/S07-Q2.png`

### C16. The live network (mainnet) launched in November 2024.

- `S11-Q1` from S11, Redbelly Network: "2024-11-28 [...] Redbelly Mainnet is now LIVE!"
  - Captured automatically: `evidence/captures/S11-Q1.png`
- `S11-Q2` from S11, Redbelly Network: "has officially launched its Mainnet."
  - Captured automatically: `evidence/captures/S11-Q2.png`
- `S02-Q2` from S02, Redbelly Network: "2024 November Mainnet Launched"
  - Manual screenshot pending: `evidence/manual/S02-Q2.png`

### C17. Tokeniser is a Redbelly Network project that operates on Redbelly Network and is built for Australian funds and companies.

- `S07-Q1` from S07, Tokeniser Pty Ltd: "Tokeniser operates on Redbelly Network, Australia's public digital token infrastructure, with identity and eligibility built into the protocol."
  - Captured automatically: `evidence/captures/S07-Q1.png`
- `S07-Q2` from S07, Tokeniser Pty Ltd: "Tokeniser is a Redbelly Network project: [...] born from research at the University of Sydney and Australian Government Science Agency: CSIRO"
  - Captured automatically: `evidence/captures/S07-Q2.png`
- `S07-Q6` from S07, Tokeniser Pty Ltd: "Built for funds and companies ready to go global"
  - Captured automatically: `evidence/captures/S07-Q6.png`

## Post 7

```text
It has also been used in a central bank project. Project Acacia, run by the Reserve Bank of Australia and the Digital Finance CRC, used Redbelly as one of its networks, including for pilot digital money from the central bank. The final report came out in May 2026. 7/9
```

### C18. The Reserve Bank of Australia is Australia's central bank.

- `S05-Q1` from S05, Redbelly Network: "The Reserve Bank of Australia is Australia's central bank"
  - Captured automatically: `evidence/captures/S05-Q1.png`

### C19. Project Acacia is a joint initiative of the RBA and the Digital Finance Cooperative Research Centre.

- `S08-Q1` from S08, Reserve Bank of Australia: "Project Acacia is a joint initiative between the Reserve Bank of Australia (RBA) and the Digital Finance Cooperative Research Centre (DFCRC)."
  - Captured automatically: `evidence/captures/S08-Q1.png`
- `S04-Q1` from S04, Redbelly Network: "Project Acacia is a research initiative led by the Reserve Bank of Australia (RBA) and the Digital Finance Cooperative Research Centre (DFCRC)."
  - Captured automatically: `evidence/captures/S04-Q1.png`

### C20. Redbelly Network was one of the networks used for Project Acacia pilot use cases.

- `S10-Q1` from S10 PDF p.15 (printed p.12), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Pilot use cases were conducted on a range of public and private [...] platforms, including Canvas Connect (private), Ethereum (public), Hedera (both public and private instances), Redbelly Network (public)"
  - Captured automatically: `evidence/captures/S10-Q1.png`
- `S02-Q3` from S02, Redbelly Network: "2025 July Selected to participate in RBA Project Acacia"
  - Captured automatically: `evidence/captures/S02-Q3.png`

### C21. Pilot wholesale central bank digital currency was used on Redbelly Network in the project.

- `S10-Q2` from S10 PDF p.16 (printed p.13), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Use cases used three of the short-listed [...] platforms for their experimentation with pilot wCBDC [...] and Redbelly Network (a public-permissioned"
  - Captured automatically: `evidence/captures/S10-Q2.png`
- `S08-Q2` from S08, Reserve Bank of Australia: "Issuance of pilot wholesale CBDC for testing use cases will occur on a range of private and public-permissioned [...] platforms, including Hedera, Redbelly Network, R3 Corda, Canvas Connect and other EVM-compatible networks."
  - Captured automatically: `evidence/captures/S08-Q2.png`
- `S10-Q5` from S10 PDF p.60 (printed p.57), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Australian Bond Exchange piloted secondary market transactions involving the purchase of a tokenised corporate bond digital twin [...] using wCBDC as the settlement asset. Both the tokenised bond and the wCBDC were issued on to the same network. [...] network used in use case: Redbelly Network."
  - Captured automatically: `evidence/captures/S10-Q5.png`

### C22. The final report was released in May 2026.

- `S09-Q1` from S09, Reserve Bank of Australia: "18 May 2026 [...] today released a report detailing the findings of Project Acacia"
  - Captured automatically: `evidence/captures/S09-Q1.png`

## Post 8

```text
On Redbelly, teams led by Australian Bond Exchange, Fireblocks, Macropod and NotCentralised tested things like corporate bonds, an investment fund and a security backed by loans. To be clear: this was research, and the RBA does not endorse any participant. 8/9
```

### C23. Use cases (trials) led by ABE, Macropod, Fireblocks and NotCentralised ran on Redbelly.

- `S10-Q3` from S10 PDF p.22 (printed p.19), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Redbelly (used by ABE, Macropod, Fireblocks and NotCentralised)"
  - Captured automatically: `evidence/captures/S10-Q3.png`

### C24. Those use cases covered corporate bonds, an investment fund and a security backed by loans.

- `S10-Q5` from S10 PDF p.60 (printed p.57), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Australian Bond Exchange piloted secondary market transactions involving the purchase of a tokenised corporate bond digital twin [...] using wCBDC as the settlement asset. Both the tokenised bond and the wCBDC were issued on to the same network. [...] network used in use case: Redbelly Network."
  - Captured automatically: `evidence/captures/S10-Q5.png`
- `S10-Q6` from S10 PDF p.63 (printed p.60), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Macropod piloted two use cases. The first use case tested issuance, trading and redemption of tokenised units in a [...] wholesale managed investment scheme, with registration and [...] distribution handled through the Tokeniser platform."
  - Captured automatically: `evidence/captures/S10-Q6.png`
- `S10-Q7` from S10 PDF p.64 (printed p.61), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "network used in use cases: Redbelly Network."
  - Captured automatically: `evidence/captures/S10-Q7.png`
- `S10-Q8` from S10 PDF p.64 (printed p.61), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "NotCentralised piloted the structuring, issuance and management of a tokenised structured finance security backed by loans. [...] network used in use case: Redbelly Network."
  - Captured automatically: `evidence/captures/S10-Q8.png`

### C25. Project Acacia was research, and the RBA does not endorse any participant.

- `S05-Q2` from S05, Redbelly Network: "The RBA does not endorse any participants or technologies involved in the project."
  - Captured automatically: `evidence/captures/S05-Q2.png`
- `S04-Q2` from S04, Redbelly Network: "This does not represent a partnership, endorsement, or approval by the RBA or DFCRC."
  - Captured automatically: `evidence/captures/S04-Q2.png`
- `S04-Q1` from S04, Redbelly Network: "Project Acacia is a research initiative led by the Reserve Bank of Australia (RBA) and the Digital Finance Cooperative Research Centre (DFCRC)."
  - Captured automatically: `evidence/captures/S04-Q1.png`

## Post 9

```text
Why it matters:
Businesses can raise money and manage investors digitally, with the rules built in.
Trades can settle instantly.
The money and the asset can move together, with less back and forth.

Real assets, verified people, rules built in.

redbelly.network 9/9
```

### C26. Businesses and funds can raise money and manage investors digitally, with eligibility rules built in.

- `S07-Q6` from S07, Tokeniser Pty Ltd: "Built for funds and companies ready to go global"
  - Captured automatically: `evidence/captures/S07-Q6.png`
- `S07-Q7` from S07, Tokeniser Pty Ltd: "Lower capital costs. Faster fundraising. Better investor experience."
  - Captured automatically: `evidence/captures/S07-Q7.png`
- `S07-Q8` from S07, Tokeniser Pty Ltd: "SaaS for fund administration and investor portals."
  - Captured automatically: `evidence/captures/S07-Q8.png`
- `S07-Q3` from S07, Tokeniser Pty Ltd: "Every holder is verified and every transfer checked against the asset's rules, automatically."
  - Captured automatically: `evidence/captures/S07-Q3.png`

### C27. Trades can settle instantly.

- `S07-Q5` from S07, Tokeniser Pty Ltd: "Holders gain fractional ownership, direct custody, atomic settlement, and 24/7 secondary trading through protocol finance."
  - Captured automatically: `evidence/captures/S07-Q5.png`
- `S07-Q9` from S07, Tokeniser Pty Ltd: "T+0 [...] Settlement times"
  - Captured automatically: `evidence/captures/S07-Q9.png`
- `S06-Q2` from S06, Redbelly Network: "guarantee the impossibility of forking and mitigate double spending with near-instant finality."
  - Captured automatically: `evidence/captures/S06-Q2.png`

### C28. Money and assets can sit on the same network and move together, reducing reconciliation.

- `S10-Q5` from S10 PDF p.60 (printed p.57), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "Australian Bond Exchange piloted secondary market transactions involving the purchase of a tokenised corporate bond digital twin [...] using wCBDC as the settlement asset. Both the tokenised bond and the wCBDC were issued on to the same network. [...] network used in use case: Redbelly Network."
  - Captured automatically: `evidence/captures/S10-Q5.png`
- `S10-Q9` from S10 PDF p.28 (printed p.25), Reserve Bank of Australia and Digital Finance Cooperative Research Centre: "By integrating settlement, asset transfer and reconciliation functions on a single platform"
  - Captured automatically: `evidence/captures/S10-Q9.png`
- `S12-Q7` from S12, Redbelly Network: "Lower intermediaries and automate issuance, settlement and compliance"
  - Captured automatically: `evidence/captures/S12-Q7.png`

## Judgement calls

- Post 1 says Redbelly is a public network. The RBA final report lists it as public (S10-Q1) and public-permissioned (S10-Q2). Public is the plain word for both.
- Post 2 describes how traditional finance works, not Redbelly. It paraphrases the RBA report's description of separate institutions and manual reconciliation (S10-Q4) and makes no time claim.
- Post 3's concert ticket is an analogy. The fund unit in image 3 is labelled as an illustrative example, not a real product.
- Post 4 says privacy tech means being verified does not mean showing everyone your details. Redbelly's own wording is that participants verify their identities while privacy is protected through zero-knowledge proofs (S03-Q4).
- Post 7 says Project Acacia was run by the RBA and the Digital Finance CRC. Both RBA media releases call it a joint initiative (S08-Q1).
- Posts 7 and 8 avoid saying Redbelly partnered with, or was approved by, the RBA. Redbelly's own FAQ says it was not (S04-Q2), and post 8 says so in plain words.
- Post 9 says trades can settle instantly. This is Tokeniser's stated T+0 settlement (S07-Q9) and Redbelly's deterministic finality (S12-Q6). It is a capability, not a promise about any asset.
- No post mentions a token, a price or an investment outcome.
