# Source Pack: 04_HuggingFace最小示例

## Unit

- Course: LLM 基础与应用工程
- Unit: 04_HuggingFace最小示例
- Output: `04_HuggingFace最小示例/学习页.html`
- Snapshot / 访问日期: `2026-06-21`

## Source Boundary

This page reconstructs an existing local study page into the learning-kit 1.0
shared shell. No upstream assignment or external repository is attached in this
pass. The factual boundary is the course map, the old unit page already in the
course folder, and the public Hugging Face documentation listed below.

## Sources Used

| Source | Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | Confirms unit 04 sits after the role-boundary lesson and before the retrieval / prompt / eval / RAG chain. |
| Old unit page | `学习页.html` before reconstruction | Main teaching spine: `pipeline`, `AutoTokenizer`, `AutoModel`, `generate`, device checks, output reading, and common failure modes. |
| Course shell config | `../course-shell.json` | Shared nav contract for the page and the rest of the course. |
| Hugging Face pipeline docs | https://huggingface.co/docs/transformers/main_classes/pipelines | `pipeline` as an inference API, especially the preprocessing / model / postprocessing split. |
| Hugging Face tokenizer docs | https://huggingface.co/docs/transformers/main_classes/tokenizer and https://huggingface.co/docs/transformers/fast_tokenizers | Tokenizers prepare model inputs; `AutoTokenizer.from_pretrained()` resolves the right tokenizer class; `input_ids` and `attention_mask` are the core fields to inspect. |
| Hugging Face generation docs | https://huggingface.co/docs/transformers/main_classes/text_generation and https://huggingface.co/docs/transformers/llm_tutorial | `generate()` handles text generation; `GenerationConfig` and parameters such as `max_new_tokens` control generation behavior. |
| Hugging Face auto classes | https://huggingface.co/docs/transformers/model_doc/auto and https://huggingface.co/docs/transformers/quicktour | Auto classes pick the architecture that matches the pretrained name/path; task-specific classes such as `AutoModelForSequenceClassification` and `AutoModelForCausalLM` are the right heads for classification and generation. |
| Model outputs docs | https://huggingface.co/docs/transformers/main_classes/output | Models return `ModelOutput`-style objects that expose fields such as `logits`. |

## Source-To-Unit Notes

- Unit 04 is the bridge from the role-boundary lesson to a concrete Hugging
  Face call. It should make the learner able to tell whether a demo is using a
  standard inference helper, a manually split classification path, or an
  autoregressive generation path.
- The page should keep three paths separate: `pipeline` for a quick standard
  task, `AutoTokenizer + AutoModelForSequenceClassification` for inspecting
  logits, and `AutoTokenizer + AutoModelForCausalLM + generate` for open-ended
  continuation.
- The page should also make the common failure modes visible: wrong model
  head, mismatched tokenizer, device mismatch, over-long inputs, and confusing
  `max_length` with `max_new_tokens`.
- Any recommendation about which path to choose is an editorial recommendation,
  not a claim that Hugging Face docs force a single workflow.

## Gaps And Notes

- No public assignment or upstream repo is attached in this pass.
- The page teaches usage patterns from the docs, not a pinned provider contract.
- If future edits need version-specific behavior, record the version or commit
  separately.