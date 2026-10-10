# Data directory

Large data products are intentionally excluded from Git.

The curated Rubin alert dataset and supporting products will be distributed separately through Google Drive. After receiving the links:

1. copy `config/data_sources.example.json` to `config/data_sources.json`;
2. replace the placeholder URLs and output names;
3. run `python scripts/download_drive_data.py --config config/data_sources.json`;
4. keep the downloaded files under this directory.

Expected products may include:

```text
data/
├── hackathon_alert_catalog/
├── vsx_rubin_matches/
├── vsx_gaia_counterparts/
└── metadata/
```

The exact filenames and schema should be documented when the dataset is released.

Do not commit large datasets, authentication cookies, or private Google Drive links.
