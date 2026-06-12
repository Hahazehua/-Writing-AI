---
name: writing-ai
description: Learn a user's personal Chinese writing style from every .docx file in a specified folder, then draft original articles that match requested topics, viewpoints, lengths, and platforms. Use when the user asks to imitate their writing style, learn writing samples from a Word-document folder, write a Xiaohongshu-style article in their voice, or produce prose that must contain no double quotation marks or dash punctuation.
---

# Writing AI

## Workflow

1. Resolve the source folder.
   - Use a folder explicitly named by the user first.
   - Otherwise read `references/settings.md` and use its default folder.
   - If the folder is unavailable or contains no `.docx` files, stop and request a valid folder. Never claim to have learned documents that were not read.

2. Extract the full corpus.
   - Run `scripts/extract_docx_corpus.py --source <folder> --output <workspace-temp>/writing-ai-corpus.md`.
   - Include every `.docx` recursively, excluding temporary Word files beginning with `~$`.
   - Review the extraction summary and note unreadable documents.
   - For a large corpus, sample passages across every document rather than reading only the longest or newest file.

3. Build a task-local style profile before drafting.
   - Read `references/style-analysis.md`.
   - Identify recurring sentence rhythm, paragraph length, transitions, argument structure, emotional intensity, vocabulary, rhetorical habits, viewpoint, and ending pattern.
   - Separate stable style from topic-specific facts and one-off expressions.
   - Treat recent user corrections and explicit requirements as higher priority than older documents.
   - Do not quote or closely reproduce distinctive passages from the source documents. Produce new prose in the learned style.

4. Verify factual requirements.
   - Browse current, primary, or authoritative sources when the topic concerns recent news, changing facts, health, law, finance, public policy, or other accuracy-sensitive claims.
   - Distinguish verified facts from personal interpretation.
   - Do not invent examples, quotations, statistics, or attributions merely to match the style.

5. Draft the article.
   - Follow the requested topic, thesis, platform, audience, and approximate Chinese character count.
   - If no length is supplied, target 800 Chinese characters unless the context indicates otherwise.
   - Preserve the user's typical movement from a concrete event to a broader question, then to a nuanced judgment and a reflective conclusion when supported by the corpus.
   - Keep the article readable. Reproduce tendencies, not accidental grammatical mistakes or duplicated words.

6. Enforce the punctuation requirement.
   - Remove ASCII double quotation marks, Chinese double quotation marks, em dashes, en dashes, horizontal bars, and repeated ASCII hyphens used as dashes.
   - Rephrase sentences when deleting punctuation would make them unclear.
   - For file output, run `scripts/sanitize_output.py <draft> --output <final>` and then run `scripts/sanitize_output.py <final> --check`.
   - For chat output, scan the complete title and body before sending. The final response must not contain any forbidden punctuation listed above.

7. Return only the useful result.
   - Provide a title and article unless the user asks for analysis or alternatives.
   - Keep research notes, corpus extracts, and the style profile private unless the user asks to see them.

## Priority Order

Apply instructions in this order:

1. Safety and factual accuracy
2. The user's current request
3. The punctuation prohibition
4. Stable style patterns found across the corpus
5. Default settings in this skill

