# Source Pack: Tokenizer 与 token 流

## Source Boundary

- Course: 从零训练小语言模型
- Unit: 02 Tokenizer 与 token 流
- Snapshot: 2026-06-21
- Access date: 2026-06-21
- Local inputs: course-root `index.html`, current unit page `学习页.html`, and the neighboring unit 01 page for scope alignment.

## Source-To-Unit Notes

- The course index places this unit immediately after the language-modeling objective and before the Transformer unit, so this page should teach the input contract between raw text and the training loop, not tokenizer implementation internals.
- Stanford CS336 Spring 2025 describes the course as implementation-heavy and lists Assignment 1 components including tokenizer, model architecture, and optimizer. The lecture trace also frames language-modeling data as a sequence of integers output by the tokenizer. Use CS336 as the public source name for the “text becomes integer sequence” boundary.
- Hugging Face Tokenizers documentation names the public tokenization pipeline stages: normalization, pre-tokenization, model, post-processing, and decoding. It also notes truncation, padding, and special-token handling as part of the tokenizer toolchain. Use this source for the stage order and terminology, not for proprietary implementation details.
- `llm.c` README shows a concrete training artifact boundary: tokenized datasets, a GPT-2 tokenizer, `.bin` files with a short header and token stream, and tests that compare the C path with the PyTorch reference. Use this source for file-boundary and validation examples.
- Ai2’s OLMo 2 blog defines “fully open” as releasing weights, training data, code, and evaluation together. Use this as the public reference for why tokenizer choice, special-token inventory, and exported artifacts should stay inspectable.

## Unit Boundary

- This page covers: tokenizer purpose, tokenization pipeline stages, subword intuition, token id contracts, token streams, special tokens, padding/EOS, `.bin`-style token artifacts, and the checks that catch misalignment.
- This page does not cover: full tokenizer training code, model-side embedding math, Transformer internals, optimizer scheduling, GPU performance tuning, or scaling-law analysis. Those belong to later units.
- Keep the anchor example at the level of a short mixed-language sentence plus a token stream window. Do not expand it into a tokenizer implementation lesson.

## Gaps

- No local tokenizer training script, raw corpus snapshot, or exact binary-file writer was provided for this unit, so avoid claiming any repository-specific command or file layout beyond what the cited public sources already support.
- Do not infer exact merge-table behavior, normalization rules, or token ids for a specific checkpoint unless the page shows them as examples only.
- If later work needs a concrete tokenizer recipe or repository commands, create a new source pack for that unit instead of stretching this one.
