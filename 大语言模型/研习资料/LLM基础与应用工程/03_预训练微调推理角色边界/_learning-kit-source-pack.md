# Learning Kit Source Pack

## Unit

- Course: LLM 基础与应用工程
- Unit: 03｜预训练、微调、推理的角色边界
- Output: `03_预训练微调推理角色边界/学习页.html`
- Snapshot / access date: 2026-06-21

## Source Boundary

This page is a reconstruction of an existing local study page into the
learning-kit 1.0 shared shell. No external web source was added in this pass.
The factual and instructional boundary is the course map plus the old unit page
already present in the course folder.

## Sources Used

| Source | Path | Supports |
| --- | --- | --- |
| Course index | `../index.html` | Course sequence, unit role, previous and next lesson context. Unit 03 follows tokenizer/Transformer foundations and prepares for the HuggingFace minimal example. |
| Old unit page | `学习页.html` before reconstruction | Main teaching claims: pretraining changes base parameters, fine-tuning adapts behavior with smaller targeted data, inference uses fixed parameters with prompt/context/decoding controls, and application roles include embedding, reranking, and generation. |
| Course shell config | `../course-shell.json` | Shared navigation contract and page registration for hosted course pages. |
| Shared runtime assets | `../assets/study-page.css`, `../assets/study-page.js`, local KaTeX/Prism assets | Visual shell, navigation progress, copy buttons, local checks, terminal lab, shape/data-flow tracer, and export behavior. |

## Source-To-Unit Notes

- The course index says this unit exists to separate training, adaptation, and
  calling boundaries before the learner runs a concrete HuggingFace example.
- The old unit page already contains the useful domain spine: pretraining,
  fine-tuning, inference, embedding, reranking, generation, RAG decision
  choices, temperature controls, and common misconception diagnosis.
- The reconstruction should preserve that spine while making it more
  inspectable: use a role/state table, a lifecycle tracer, a small decoding
  failure lab, code snippets, and grouped diagnostic practice with feedback.
- The page should not claim that fine-tuning, RAG, or decoding parameters solve
  every quality problem. The learner should first classify the failure mode:
  missing evidence, unstable format, weak retrieval, poor ranking, sampling
  randomness, or stable task behavior that may justify fine-tuning.

## Unit Role

This is a normal-to-deep technical foundation unit. It bridges model internals
to application engineering decisions:

1. Unit 01 explains how text enters the model.
2. Unit 02 explains how Transformer/attention reads context.
3. Unit 03 explains which stage changes parameters, which stage changes the
   current input/context, and which application call role solves which part of
   a pipeline.
4. Unit 04 can then show a concrete HuggingFace call without blurring training
   and inference.

## Known Gaps

- No public upstream textbook, lecture, or assignment source is attached to this
  local course page in this pass.
- Concrete commands are limited to minimal illustrative API-style snippets; they
  are not presented as an official assignment interface.
- Mutable model/provider details are intentionally avoided. The page teaches
  role boundaries rather than a vendor-specific API contract.
