# Source Pack: 05_embedding_reranking_generation边界

## Unit

- Course: LLM 基础与应用工程
- Unit: 05_embedding_reranking_generation边界
- Output: `05_embedding_reranking_generation边界/学习页.html`
- Snapshot / 访问日期: `2026-06-21`

## Source Boundary

This page reconstructs the existing local study page into the learning-kit 1.0 shared shell. No upstream assignment or external repository is attached in this pass. The factual base is the course map, the old local unit page already present in the folder, and the official documentation links listed below.

## Sources Used

| Source | URL / Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | Confirms the unit sits after 04 and before 06, and anchors the course sequence. |
| Old unit page | `学习页.html` before reconstruction | Main teaching spine: embedding retrieval, reranking, generation, failure diagnosis, and practice structure. |
| Course shell config | `../course-shell.json` | Shared nav contract for this page and the rest of the course. |
| Hugging Face pipeline docs | https://huggingface.co/docs/transformers/main_classes/pipelines | Pipeline as an inference wrapper and the preprocessing / model / postprocessing split. |
| Hugging Face tokenizer docs | https://huggingface.co/docs/transformers/main_classes/tokenizer and https://huggingface.co/docs/transformers/fast_tokenizers | Tokenizers prepare model inputs, produce fields such as `input_ids` and `attention_mask`, and expose fast tokenization behavior. |
| Hugging Face auto classes | https://huggingface.co/docs/transformers/model_doc/auto and https://huggingface.co/docs/transformers/quicktour | Auto classes select the right architecture from a pretrained name or path; useful for explaining route choice. |
| Hugging Face generation docs | https://huggingface.co/docs/transformers/main_classes/text_generation and https://huggingface.co/docs/transformers/generation_strategies | `generate()`, decoding strategies, and common generation pitfalls such as `max_new_tokens` vs `max_length`. |
| Hugging Face output docs | https://huggingface.co/docs/transformers/main_classes/output and https://huggingface.co/docs/transformers/internal/generation_utils | `ModelOutput` structure, fields such as `logits`, and the shape of generation outputs. |
| Sentence Transformers semantic search | https://www.sbert.net/examples/sentence_transformer/applications/semantic-search/README.html | Bi-encoder embeddings for semantic search and first-stage retrieval. |
| Sentence Transformers retrieve & re-rank | https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html and https://www.sbert.net/examples/cross_encoder/applications/README.html | Two-stage retrieval, top-k reranking, and the role split between bi-encoder and cross-encoder. |
| Sentence Transformers cross-encoder docs | https://www.sbert.net/docs/cross_encoder/usage/usage.html and https://www.sbert.net/docs/package_reference/cross_encoder/model.html | Sentence-pair scoring, reranker behavior, and the fact that Cross-Encoders do not produce sentence embeddings. |

## Source-To-Unit Notes

- Unit 05 should teach that embedding / bi-encoder is the first-stage retriever, Cross-Encoder is the reranker, and generation is the answer writer.
- The page should show one traceable query path from text to embeddings, candidate retrieval, reranking, prompt assembly, and answer generation.
- The page should make failure modes visible: reranking too many pairs, confusing semantic similarity with truth, letting generation replace evidence, and not logging query / candidate / context / answer.
- Any recommendation about which route to prefer is an editorial recommendation, not a claim that the docs force a single workflow.

## Gaps And Notes

- No public assignment or upstream repository is attached in this pass.
- If future edits depend on version-specific behavior, re-check the docs snapshot or access date.
