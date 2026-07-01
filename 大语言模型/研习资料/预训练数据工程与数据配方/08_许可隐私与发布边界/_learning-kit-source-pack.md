# Source Pack: 许可、隐私与发布边界

## Source Boundary

- Course: 预训练数据工程与数据配方
- Unit: 08_许可隐私与发布边界
- Snapshot: access date 2026-06-22
- Source types: existing course index, neighboring unit pages, and the public sources listed below.

## Source-To-Unit Notes

- This unit sits after 07_可复现流水线与运行记录 and closes the course.
- The learner should already understand pipeline reproducibility, manifests, checkpoints, and replay boundaries.
- The page should separate four related but different decisions:
  - license check: whether the source allows training, copying, or redistribution
  - privacy check: whether the content can be retained without creating an avoidable re-identification risk
  - release boundary: what can be public, restricted, or internal only
  - audit trail: what evidence supports the decision and how a deletion request can be handled later
- The teaching emphasis should be:
  - public visibility is not the same as permission
  - anonymization is stronger than replacing names with placeholders
  - open weights do not imply open training data
  - a release decision should stay tied to a specific source, use, and evidence set

## Source Facts

- Creative Commons guidance explains that a visible page or downloadable item is not automatically a free reuse grant, and that the license text controls the allowed uses.
- GDPR guidance emphasizes lawful processing, data minimization, transparency, and security, which are the right conceptual buckets for privacy review.
- NIST AI RMF and the NIST Privacy Framework both treat privacy and model risk as governance problems that need mapping, measurement, and management rather than only technical masking.
- Hugging Face dataset cards and model cards show how source, license, limitation, and risk summaries are commonly documented in public model and dataset releases.

## Public Source Context

- Creative Commons FAQ:
  https://creativecommons.org/faq/index.html
- Creative Commons content mining guide:
  https://wiki.creativecommons.org/wiki/Content_mining
- GDPR text:
  https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32016R0679
- European Commission GDPR principles overview:
  https://commission.europa.eu/law/law-topic/data-protection/rules-business-and-organisations/principles-gdpr/overview-principles/what-data-can-we-process-and-under-which-conditions_en
- NIST AI RMF 1.0:
  https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-ai-rmf-10
- NIST Privacy Framework:
  https://www.nist.gov/privacy-framework
- Hugging Face Dataset Cards:
  https://huggingface.co/docs/hub/datasets-cards
- Hugging Face Model Cards:
  https://huggingface.co/docs/hub/model-cards

## Gaps

- No upstream unit handout is available in this workspace for this page.
- Treat the exact threshold examples and the release-gate YAML as teaching examples unless a cited source states them directly.
- Treat the course's release recommendations as editorial synthesis when they combine licensing, privacy, and publishing guidance.
- The page should not claim that a single jurisdictional rule or policy solves every release decision; it should show how to record the evidence needed for the project at hand.
