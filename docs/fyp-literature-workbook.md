# FYP Literature Workbook

> **Purpose:** Working instrument for the future formal proposal. It contains no
> completed literature review and deliberately invents no authors, papers, dates,
> venues, DOIs or URLs. Verify every source yourself.

## 1. Evidence authority and workflow

For each candidate claim:

1. identify the exact proposition;
2. decide whether it needs an official specification, primary academic study,
   security guidance, statistical method source, or secondary background;
3. search more than one database/source channel;
4. open and read the source—not only its abstract or search snippet;
5. record method, dataset, limitations and the page supporting the claim;
6. compare with the closest work;
7. update the claim tracker with safe wording;
8. never infer novelty from failure to find a result in one search.

Use these proposal labels: `[LITERATURE-REQUIRED]`, `[SUPERVISOR-DECISION]`,
`[UNIVERSITY-REQUIREMENT]`, `[FUTURE-RESEARCH]`, and `[DO-NOT-CLAIM]`.

## 2. Literature search matrix

| ID | Topic | Search questions | Suggested search terms | Source types | Why needed | Proposal section |
|---|---|---|---|---|---|---|
| L01 | MCP architecture | What are host/client/server/tool roles and discovery semantics? Which fields are normative? | `Model Context Protocol specification tools list tool definition inputSchema annotations` | **Official specification**, official documentation; primary academic context | Accurate system background and scope | Background, terminology, architecture |
| L02 | MCP security | What trust, authorization, metadata and transport risks are documented? | `MCP security threat model tool metadata authorization guidance` | Official security guidance + primary academic security sources | Establish concern without speculation | Problem, threat model, significance |
| L03 | MCP tool poisoning | How is tool poisoning defined? Does it require intent or observed agent influence? | `MCP tool poisoning malicious tool description attack` | **Primary academic sources**, authoritative security research | Core construct and title choice | Problem, taxonomy, RQ |
| L04 | Tool metadata poisoning | Has instruction-bearing tool metadata been studied outside MCP? | `AI agent tool metadata poisoning tool description manipulation` | Primary research | Nearest broader work | Related work, gap |
| L05 | Prompt injection | What are accepted definitions/taxonomies and evaluation practices? | `LLM prompt injection taxonomy attack defense evaluation` | Peer-reviewed primary/review sources | Distinguish concepts | Background, terminology |
| L06 | Indirect prompt injection | How does external content influence agents/models? | `indirect prompt injection external content agent tools` | Primary academic work | Connect metadata pathway | Background, threat model |
| L07 | Agentic AI security | What assets, trust boundaries and attacker capabilities recur? | `agentic AI security threat model tool use autonomous agents` | Primary work + authoritative security guidance | Formal threat model | Problem, methodology |
| L08 | AI tool trust | How are tool descriptions/capabilities verified and constrained? | `LLM agent tool trust capability description selection security` | Primary academic work | System positioning | Background, related work |
| L09 | Static analysis | What properties and limitations define static security analysis? | `static security analysis configuration metadata rule based` | Recognized conference/journal sources, textbooks if permitted | Method rationale | Methodology, design |
| L10 | Rule-based detection | What are explainability, maintenance, FP/FN and evasion trade-offs? | `rule based security detector explainability false positive evasion` | Primary empirical work | Defend/limit approach | Design, discussion |
| L11 | JSON Schema security | Can invalid/inconsistent schemas create security or interoperability risk? | `JSON Schema validation security inconsistent implementation malformed schema` | Standards, official docs, primary security work | Position SCH rules and R08 | Taxonomy, limitations |
| L12 | Schema/capability mismatch | How is declared-versus-actual capability inconsistency analyzed elsewhere? | `capability mismatch metadata declared behavior static analysis` | Primary security/software research | Ground mismatch construct | Taxonomy, related work |
| L13 | Integrity monitoring | What can cryptographic fingerprints and baselines establish? | `configuration integrity monitoring canonical hash baseline security` | Primary research, standards/guidance | Correct drift claims | Design, terminology |
| L14 | Configuration drift | How is drift detected/interpreted without assuming compromise? | `configuration drift detection security baseline canonicalization` | Primary empirical/guidance sources | Position baseline feature | RQ4, related work |
| L15 | Security-detector evaluation | Which metrics, prevalence and uncertainty practices are appropriate? | `security detector evaluation recall false positive rate precision prevalence confidence interval` | Primary methodology/statistics | Formal metric plan | Methodology, results |
| L16 | Holdout/preregistration | How should tuning/evaluation separation and preregistration be handled? | `machine learning security evaluation holdout contamination preregistration` | Primary methodology/open-science sources | Protect confirmatory status | Methodology, validity |
| L17 | Sample-size planning | How should N be chosen for recall/FPR CIs and paired comparisons? | `sample size sensitivity specificity confidence interval paired classifier McNemar` | Statistical primary/method sources | Avoid arbitrary N | Methodology |
| L18 | Inter-rater agreement | When is Cohen’s kappa appropriate and what are its limitations? | `Cohen kappa inter rater agreement prevalence limitations adjudication` | Statistical/methodological primary sources | Review protocol and pilot interpretation | Methodology, validity |
| L19 | Adversarial robustness | How are paraphrase, Unicode, encoding and field-relocation variations evaluated? | `adversarial robustness text detector paraphrase Unicode encoding` | Primary empirical work | Robustness plan | Method, limitations |
| L20 | Resource-exhaustion safety | How should parsers/static analyzers bound hostile inputs and output? | `resource exhaustion secure parser algorithmic complexity denial service static analyzer` | Primary security work/guidance | Justify bounds/P0 fix | Design, threat model |
| L21 | Output injection | What risks arise in terminals, spreadsheets and machine-readable reports? | `terminal escape injection CSV formula injection security report` | Authoritative security guidance + primary sources | Reporting boundary | Design/security |
| L22 | Security benchmarking | How should latency be measured and reported for static analyzers? | `static analyzer performance benchmark warmup p95 reproducibility` | Primary benchmarking methodology | Lightweight claim | Method/results |
| L23 | MCP ecosystem/adoption | Is MCP use increasing, by whom, and in what contexts? | `Model Context Protocol adoption ecosystem survey` | Official releases plus credible empirical/secondary sources | Only if making adoption/significance claims | Introduction |
| L24 | Existing MCP tools/scanners | Which products/research systems inspect MCP metadata, and how? | `MCP security scanner inspector tool poisoning detector` | Primary papers, official project docs/code | Nearest-work/novelty test | Related work/contribution |

### Search log

| Date | Matrix ID | Database/source | Exact query | Filters | Results screened | Sources retained | Notes/next query |
|---|---|---|---|---|---:|---:|---|
|  |  |  |  |  |  |  |  |

## 3. Source-quality rubric

Score each dimension 0–2; do not mechanically accept a source from total score
alone.

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Authority | anonymous/unclear | recognized practitioner/secondary | peer-reviewed primary, official spec, authoritative organization |
| Relevance | adjacent only | partial construct/method | directly answers the claim |
| Method transparency | unsupported assertion | partial method/data | reproducible method, data and analysis described |
| Evidence quality | anecdote | limited/uncertain | appropriate empirical/theoretical evidence |
| Currency/version | obsolete without reason | older but useful | current for time-sensitive MCP claims or historically foundational |
| Independence | vendor/self-promotion only | declared interest | independent or limitations/conflicts transparent |
| Claim fit | cannot support wording | supports narrower claim | directly supports exact proposition |
| Limitations | absent | briefly acknowledged | limitations/threats explicitly analyzed |

### Usage rules

- Official specifications are authoritative for protocol semantics, not for
  independent effectiveness or prevalence claims.
- Primary research should support technical and empirical claims.
- Review papers may map a field but do not replace reading critical primary work.
- Blogs, vendor pages and news can document announcements/incidents only with
  appropriate qualification.
- Search snippets, citation-count screenshots, GitHub stars and AI output are not
  scholarly evidence.
- Retain contradictory evidence and explain disagreement.

## 4. Novelty verification worksheet

Do not mark “novel” until every relevant question has evidence and supervisor
review.

- [ ] Has static inspection of MCP tool definitions already been studied?
- [ ] Has MCP tool poisoning already been operationalized or evaluated?
- [ ] Do existing MCP security scanners flag descriptions, schemas or metadata?
- [ ] Has rule-based detection been applied to agent tool metadata?
- [ ] Do existing systems perform bounded decoding of metadata representations?
- [ ] Do existing systems combine suspicious-pattern analysis with fingerprints/drift?
- [ ] Is reproducible artifact/configuration identity already standard in this area?
- [ ] Does an existing dataset overlap the proposed construct?
- [ ] Is the closest contribution algorithmic, application-specific,
  integrative, dataset-oriented, evaluative or educational?
- [ ] What exact component differs from the closest work?
- [ ] Is that difference research-significant or only implementation detail?
- [ ] Can the proposed comparison demonstrate the difference fairly?
- [ ] Have backward/forward citation chains been checked?
- [ ] Have negative and contradictory results been retained?
- [ ] Has the supervisor agreed on the defensible contribution wording?

**Current novelty status:** NOT ESTABLISHED. Use “candidate contribution.”

## 5. Empty related-work comparison table

| Work | Year | Target/problem | Method | MCP-specific? | Static/dynamic | Detection type | Dataset/population | Metrics | Main findings | Limitations | Relation to this FYP | Source verified? |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |

## 6. Paper-reading template

Copy this section once per source.

### Source ID: ______

| Field | Student record |
|---|---|
| Full verified citation |  |
| Source type / peer-review status |  |
| DOI or stable official URL |  |
| Research problem |  |
| Research question/hypothesis |  |
| Construct definitions |  |
| Threat model / assumptions |  |
| Method/design |  |
| Dataset/population and provenance |  |
| Sample size and rationale |  |
| Metrics/statistics |  |
| Main findings |  |
| Uncertainty/effect sizes |  |
| Limitations/threats to validity |  |
| Ethics/data considerations |  |
| Relation to this FYP |  |
| Agreement or conflict with other sources |  |
| Quotable idea and exact page |  |
| Student’s interpretation in own words |  |
| Claim(s) this source can support |  |
| Claim(s) this source cannot support |  |
| Follow-up sources/search terms |  |

Before using it, answer: Did I read the full source? Is my wording narrower than
or equal to the evidence? Am I confusing the authors’ interpretation with their
observed result?

## 7. Claim-to-source tracker

| Claim ID | Exact proposed claim | Seed-pack label | Required source type | Candidate source IDs | Contradictory source IDs | Exact page/evidence | Safe wording approved? | Supervisor note |
|---|---|---|---|---|---|---|---|---|
| C01 | MCP defines tool discovery and tool-definition fields | LITERATURE-REQUIRED | Official specification |  |  |  |  |  |
| C02 | Tool metadata can influence agent selection/reasoning | LITERATURE-REQUIRED | Primary academic + spec context |  |  |  |  |  |
| C03 | Tool poisoning is distinct from/related to indirect prompt injection | LITERATURE-REQUIRED | Primary construct sources |  |  |  |  |  |
| C04 | The proposed taxonomy represents a defensible target construct | SUPERVISOR-DECISION | Literature synthesis |  |  |  |  |  |
| C05 | Static rule-based analysis is appropriate for this research question | LITERATURE-REQUIRED | Static/detector method sources |  |  |  |  |  |
| C06 | Existing MCP defenses leave a candidate metadata-inspection gap | LITERATURE-REQUIRED | Systematic nearest-work search |  |  |  |  |  |
| C07 | Precision/recall/FPR/CIs are appropriate metrics | LITERATURE-REQUIRED | Detector/statistics methods |  |  |  |  |  |
| C08 | Proposed N is statistically justified | SUPERVISOR-DECISION | Sample-size method + assumptions |  |  |  |  |  |
| C09 | Reviewer protocol produces credible labels | SUPERVISOR-DECISION | Annotation/agreement methods |  |  |  |  |  |
| C10 | “Lightweight” is justified at the selected boundary | FUTURE-RESEARCH | Benchmark methods + future results |  |  |  |  |  |
| C11 | Fingerprinting/drift integration is a candidate contribution | LITERATURE-REQUIRED | Integrity/drift nearest work |  |  |  |  |  |
| C12 | The formal FYP contribution is novel/significant | DO-NOT-CLAIM yet | Complete related-work synthesis |  |  |  | No |  |

## 8. Citation and synthesis checks

- [ ] Every external factual sentence has an appropriate source.
- [ ] Official MCP semantics cite the official specification/version.
- [ ] Definitions use primary/authoritative sources and acknowledge disagreements.
- [ ] No citation is copied from another paper without opening the original.
- [ ] No quotation lacks an exact page/section.
- [ ] Paraphrases use the student’s words and preserve the source meaning.
- [ ] Related work compares target, method, data, metrics and limitations—not
  only feature lists.
- [ ] Pilot repository evidence is cited as preliminary project evidence, not
  external literature.
- [ ] Negative and null findings are included.
- [ ] Novelty language remains absent until the checklist and supervisor review.
- [ ] The final format follows the university’s required citation style.

## 9. Supervisor literature decisions

| Decision | Options to discuss | Why it changes the search |
|---|---|---|
| Core construct | suspicious metadata / narrow tool poisoning / split outcomes | Determines definitions and nearest work |
| Main contribution | detector effectiveness / secure design / integrity / reproducibility | Determines literature depth by field |
| Comparison | v0.2 / lexical baseline / ablation / external system | Requires fair comparable sources |
| Data population | synthetic/real-world/mixed | Changes ethics, provenance and external-validity literature |
| Statistics | CI precision / paired comparison / descriptive pilot | Changes sample-size and analysis sources |
| Robustness | core RQ / secondary / development-only | Changes adversarial literature burden |

## 10. Completion gate

The literature phase is not complete until the student can:

1. define the approved construct from sources rather than project intuition;
2. name and compare the closest verified work;
3. state what is genuinely different without exaggeration;
4. justify the method, metrics, data and review protocol;
5. show contradictory evidence and limitations;
6. replace every `[CITATION NEEDED — ...]` placeholder in the eventual proposal;
7. obtain supervisor agreement on contribution wording.

Until then, this workbook is planning material and no novelty claim is valid.
