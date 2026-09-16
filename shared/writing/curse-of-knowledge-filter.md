# Curse-of-Knowledge Filter

Once you know something, it becomes hard to imagine not knowing it. The result
in writing is skipped steps, unexplained terms and locations the reader cannot
find. Run this filter over every explanation and procedure before handing it
over. It is a rewrite pass, not a style preference.

## Filter questions

For each sentence that asks the reader to know, find or do something:

1. **Skipped step.** Would a first-time reader have to do or decide something
   between this step and the next? Write it out. "Open Settings" becomes
   "Select the gear icon in the top-right corner to open Settings."
2. **Unlocated object.** Does the sentence name a button, menu, file, field,
   command or page without saying where it is? Add the location, the path, or
   the exact label as the reader sees it, in the reader's interface language.
3. **Unshared term.** Does the sentence use a term, abbreviation or product
   name the target audience may not use in the same sense? Replace it with the
   glossary term, define it at first use, or remove it.
4. **Assumed state.** Does the step only work if something was already
   installed, enabled, logged in, selected or saved? Move that condition into
   the prerequisites or state it in the step.
5. **Invisible result.** After the reader acts, what should they see? If the
   text does not say, add the observable result so the reader knows it worked.
6. **Expert shortcut.** Does the text rely on a keyboard shortcut, alias,
   jargon or a "simply" or "just" that hides difficulty? Give the full path
   first; the shortcut is optional information.

## Audience calibration

Define the reader once, at the top of the document or plan: role, what they
already know, what they are trying to achieve, and which interface or version
they use. Judge every filter question against that reader, not against
yourself or a colleague. When the audience is mixed, write for the least
experienced reader who is expected to succeed and give experts a way to skip
ahead, such as a short summary or a reference table.

## Evidence for the pass

The filter is complete when a sample of the text was read as the defined
reader, each finding was rewritten, and the terms, locations and prerequisites
added are consistent with the glossary and the rest of the document. Record
that the pass was made in the chunk frontmatter or the review report; do not
claim it from intent.
