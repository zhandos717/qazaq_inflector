# Changelog

## [0.5.0] - 2026-10-05

### Added
- `predicate(word, person)` — personal predicate endings: `студентпін`, `Нұрлансың`, `қазақпыз`, `оқушысыңдар`.
- Plural pronouns `сендер`, `сіздер`, `олар` in `inflect()` and as owners in `genitive_phrase()`: `сендердің балаларың`.

### Fixed
- Feminine surnames `-ова/-ева` with a front-vowel stem took front suffixes: `Ахметоваге` → `Ахметоваға`.

## [0.4.0] - 2026-10-05

### Added
- Second person plural owners in `possessive()`: `2pl` (сендердің) and `2pl_formal` (сіздердің) — `Арналарың`, `Арналарыңыз`.
- `plural=True` in `possessive()` for several possessed items: `Арналарым`, `Нұрландары`.
- `genitive_phrase(owner, thing, case)` for possessive phrases: `Нұрланның әкесі`, `менің кітабым`.
- `strict=True` constructor option: raises `ValueError` on an unknown case or person.
- `py.typed` marker for type checkers.
- GitHub Actions workflow that publishes to PyPI via Trusted Publishing on a GitHub release.

### Fixed
- Final `п`, `к`, `қ` are voiced before vowel suffixes: `кітабы`, `Сұлтанбегі`.

### Changed
- `project.license` uses an SPDX string; the deprecated license classifier is removed.

## [0.3.0] - 2026-10-05

### Added
- `possessive(name, person, case)` for `1sg`, `2sg`, `2sg_formal`, `1pl`, `3` with case endings.

## [0.2.0] - 2026-10-05

### Fixed
- Case suffixes chosen by final sound class: vowel, nasal, sonorant, `ж/з`, voiceless.
- Ablative after `м/н/ң` (`Нұрланнан`), locative after `н` (`Нұрланда`), genitive and accusative after vowels, instrumental after `ж/з`.
- Plural suffixes `-лар/-дар/-тар`.
- Harmony of `-ов/-ев` surnames (`Құнанбаевқа`).

### Changed
- `pyproject.toml` replaces `setup.py`; Python 3.9+.
- English README; Russian and Kazakh versions in `README_RU.md`, `README_KZ.md`.

## [0.1.0] - 2025-04-24

- Initial release.

[0.5.0]: https://github.com/zhandos717/qazaq_inflector/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/zhandos717/qazaq_inflector/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/zhandos717/qazaq_inflector/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/zhandos717/qazaq_inflector/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/zhandos717/qazaq_inflector/releases/tag/v0.1.0
