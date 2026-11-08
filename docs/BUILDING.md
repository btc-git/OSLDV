# Building OSLDV from Source

[README](../README.md) | [Technical reference](TECHNICAL.md) | [Export and audit reference](EXPORTING.md)

Run the commands below from the repository root, not from `docs/`.

## Source Development Requirements

- Python 3.11+
- Node.js for the GeoLibre plugin contract test

Reproducible Windows release builds require Python 3.11.3 and the complete
`requirements-build.txt` lock. See `requirements.txt` for runtime versions and
`THIRD_PARTY_NOTICES.md` for the dependency inventory.

The files are available at [requirements-build.txt](../requirements-build.txt),
[requirements.txt](../requirements.txt), and
[THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md).

## Setup & Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. Run from source:
   ```bash
   python app.py
   ```

## Run Tests

```bash
python -m unittest discover -s tests -v
node tests/test_plugin_simplified_chrome.mjs
node --check tools/plugin_performance_harness.mjs
```

See [the test suite](../tests/README.md) for coverage and
[manual diagnostics](../tools/README.md) for developer utilities.

## Building the Executable

Before each release:
- Update `APP_VERSION` in [version.py](../version.py).
- Match `ProductVersion` in [version_info.txt](../version_info.txt), and update its
  `filevers`, `prodvers`, and `FileVersion` numeric values. For example,
  `2.0.0-beta.4` uses `(2, 0, 0, 4)` and `2.0.0.4`.
- Update the version footer in [README.md](../README.md) and add the release entry in
  [CHANGELOG.md](../CHANGELOG.md). Keep historical entries unchanged.
- After building, confirm the app's displayed version and the executable's
  Properties > Details match the intended release, then use the same version
  for the GitHub release and tag. Viewer and plugin versions are independent.

1. Use Python 3.11.3.
2. Install the complete pinned build environment:
   ```bash
   python -m pip install -r requirements-build.txt
   ```
3. Build the executable:
   ```bash
   python -m PyInstaller --clean app.spec
   ```
4. Find the executable in the `dist/` directory (the file will be named `OSLDV.exe`)

Always build through `app.spec`; it packages the icon, version metadata,
timezone and XLS support, bundled GeoLibre viewer and plugin, and license files.

The tracked specification is [app.spec](../app.spec). The executable is not
code-signed. To calculate its SHA-256 without modifying it:

```powershell
Get-FileHash -Algorithm SHA256 .\dist\OSLDV.exe
```

For a downloaded build, compare its hash with the checksum supplied for that
build before running it. Computing a hash alone does not establish trust.
