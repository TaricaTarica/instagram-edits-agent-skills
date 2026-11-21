# Contributing

Thanks for helping keep these skills accurate. Edits for Mac updates often and its automation server is undocumented, so the most valuable contributions are **verified observations**.

## Report an Edits update that broke something

Open an issue with the "Edits update broke a skill" template and include:

- Edits version (Edits → About) and `schemaVersion` from `getCapabilities`
- The skill and the line that is now wrong
- The exact tool call and the exact error text
- What worked instead, if you found it

## Share a quirk or a better default

Use the "New quirk or better default" template. Numbers beat opinions: say what you measured (frames, LUFS, retention) and on what footage.

## Pull requests

- One topic per PR. Keep each `SKILL.md` focused on its stage; put long references under the skill's `references/` folder.
- Keep descriptions in third person, saying what the skill does and when to use it, with the phrases users actually type.
- Never commit footage, tokens, personal data, or brand/company names that aren't needed to describe the app.
- If you changed tool names or params, note the Edits version in `CHANGELOG.md`.

## Maintainers: checking a new Edits release

```bash
python3 maintainer/check_edits_tools.py           # diff live tools vs snapshot (open a project for editor tools)
python3 maintainer/check_edits_tools.py --update  # after updating the skills
```

Then update the "Tested with" line in the README and add a dated CHANGELOG entry.
