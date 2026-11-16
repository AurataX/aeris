# Fluid interface library

Open `index.html` in a modern browser. It works offline and contains its prompt data; there is no installation or API key. Search by words or filter by product, interaction and task. Read a prompt, copy it or save it as text. If clipboard permission is unavailable, the text is selected for manual copying.

## Contents

- `index.html`: searchable browser for 1,200 prompts.
- `prompts.json`: all prompts with stable IDs and category metadata.
- `by-domain/`: 20 Markdown files with 60 prompts each.
- `master-brief.md`: reusable design and engineering brief.
- `research.md`: sourced research, corrections to the supplied reply and library comparisons.
- `toolkit-prompts.md`: additional focused research/implementation prompts for Apple, GNOME and named web libraries.
- `visual-direction.md` and `reference.png`: the approved atmosphere, material direction and supplied reference image.
- `validation.json`: checks performed on the prompt browser and explicit limits.

Start with `index.html` after extracting the ZIP. Markdown reference documents can be opened in any text or Markdown editor.

The 1,200 entries are systematically composed from **20 domain briefs × 15 interaction briefs × four tasks**. Every entry includes a concrete object, domain constraint, required states, acceptance criteria and an output contract. Common principles are intentionally repeated so entries work independently. They are not 1,200 independently researched libraries or 1,200 unrelated design concepts.

## How to use it

1. Read the research and fill the inputs in the master brief for your product.
2. Choose a domain similar to your actual work; replace fictional sample content.
3. Begin with Explore / Workspace composition. Settle the structure before effects.
4. Use Build for one interaction at a time, then Review and Validate for the same interaction.
5. Consult the toolkit prompts when choosing or evaluating a specific library.

Do not paste all 1,200 prompts into one coding request. That would introduce contradictory contexts and unnecessary scope. Use the master brief plus one focused prompt; retain decisions between passes.

Research checked 1 October 2026. Library APIs and licenses can change. No dependencies were installed into your product, and no product code was modified. The prompt browser is a reading tool, not a benchmarked demonstration of the proposed product architecture or motion.
