# Variable Stars in Rubin Alerts with VSX and Gaia DR3

This repository contains tutorial notebooks and reproducible workflows for working with known variable stars in the public Rubin Alert Archive using LINCC Frameworks tools.

The project combines:

- **AAVSO VSX** for variable-star identifiers, classifications, periods, and catalog metadata;
- **Gaia DR3** for astrometry, parallaxes, proper motions, photometry, and quality indicators;
- **Rubin alert products** for alert detections and historical forced-source measurements;
- **LSDB and HATS** for scalable spatial searches, crossmatching, and local catalog products.

The tutorials support two main scientific directions:

1. identifying unusual or inconsistent behavior among known variable stars;
2. preparing RR Lyrae and other pulsating-variable samples for period and distance analysis.

## Repository structure

```text
.
├── README.md
├── environment.yml
├── requirements.txt
├── .gitignore
├── notebooks/
│   ├── 01_guided_VSX_Gaia_Rubin_tutorial.ipynb
│   └── 02_home_data_download_and_crossmatch.ipynb
├── scripts/
│   └── download_drive_data.py
├── config/
│   └── data_sources.example.json
├── data/
│   └── README.md
└── results/
    └── .gitkeep
```

## Notebooks

### 1. Guided tutorial

`notebooks/01_guided_VSX_Gaia_Rubin_tutorial.ipynb`

This notebook introduces the complete regional workflow:

- opening VSX, Gaia DR3, and the public Rubin Alert Archive;
- performing spatial crossmatches;
- normalizing crossmatch columns;
- extracting `prvDiaForcedSources`;
- plotting an alert-history light curve;
- preparing anomaly-detection and RR Lyrae distance-analysis branches.

### 2. Home data-download workflow

`notebooks/02_home_data_download_and_crossmatch.ipynb`

This notebook is intended for participants to run on their own computers. It supports:

- `MODE = "test"` for a one-degree ECDFS validation run;
- `MODE = "full"` for processing the full overlap represented in the public catalogs;
- writing local HATS products with restartable output;
- reopening the local VSX–Rubin and VSX–Gaia products;
- extracting and plotting example forced-source histories.

In full mode, the notebook does **not** copy every Rubin alert indiscriminately. It searches the complete public alert archive and writes the alerts spatially associated with VSX sources under the adopted crossmatch criteria.

## Hackathon dataset from Google Drive

A curated, hackathon-ready Rubin alert product will be shared separately through Google Drive. The repository does not store the large data files directly.

After the Drive links are published:

1. copy `config/data_sources.example.json` to `config/data_sources.json`;
2. replace the placeholder URLs and filenames;
3. run the download script;
4. verify that the downloaded products appear under `data/`.

```bash
cp config/data_sources.example.json config/data_sources.json
python scripts/download_drive_data.py --config config/data_sources.json
```

The shared dataset should be described as a **curated Rubin alert product prepared for the hackathon**, not as the complete Rubin Alert Archive.

## Installation with Conda

### 1. Install Conda or Miniforge

If Conda is not already available, install Miniforge or another Conda distribution appropriate for your operating system.

### 2. Create the environment

From the repository root:

```bash
conda env create -f environment.yml
```

Activate it:

```bash
conda activate lincc-rubin
```

### 3. Register the Jupyter kernel

```bash
python -m ipykernel install \
  --user \
  --name lincc-rubin \
  --display-name "Python (LINCC Rubin)"
```

### 4. Verify the installation

```bash
python -c "import lsdb, hats, nested_pandas, astropy, dask; print('Environment ready')"
```

Check dependency consistency:

```bash
python -m pip check
```

### 5. Start JupyterLab

```bash
jupyter lab
```

Open a notebook and select:

```text
Kernel → Change Kernel → Python (LINCC Rubin)
```

## Alternative installation with pip

Conda is recommended for this workshop. If Conda cannot be used, create a clean Python 3.12 virtual environment and install:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m ipykernel install \
  --user \
  --name lincc-rubin-venv \
  --display-name "Python (LINCC Rubin venv)"
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Downloading the Drive dataset

The script accepts public Google Drive file links, folder links, or file IDs through the JSON configuration file.

Example configuration:

```json
{
  "downloads": [
    {
      "name": "hackathon_alert_catalog",
      "url": "REPLACE_WITH_PUBLIC_GOOGLE_DRIVE_FILE_URL",
      "output": "data/hackathon_alert_catalog.zip",
      "unpack": true
    },
    {
      "name": "supporting_products",
      "url": "REPLACE_WITH_PUBLIC_GOOGLE_DRIVE_FOLDER_URL",
      "output": "data/supporting_products",
      "folder": true,
      "unpack": false
    }
  ]
}
```

Run:

```bash
python scripts/download_drive_data.py \
  --config config/data_sources.json
```

To replace an existing download:

```bash
python scripts/download_drive_data.py \
  --config config/data_sources.json \
  --overwrite
```

The Google Drive files or folders must be shared so that participants can access them. Do not commit private credentials or browser cookies to this repository.

## Recommended participant workflow

### Before the hackathon analysis session

1. Clone the repository.
2. Create and activate the Conda environment.
3. Register the Jupyter kernel.
4. Run the guided notebook from the beginning.
5. Keep the home notebook in `MODE = "test"`.
6. Confirm that VSX, Gaia DR3, and Rubin can be accessed.
7. Confirm that local HATS products can be written and reopened.

### After the curated dataset is shared

1. Add the public Drive links to `config/data_sources.json`.
2. Download the products with `scripts/download_drive_data.py`.
3. Inspect `data/README.md` and any dataset-specific metadata.
4. Use the common curated product for the scientific analysis.
5. Store generated tables and figures under `results/`.

## Data provenance

The final analysis may combine three different provenance levels:

- **Original survey products:** public Rubin alert products;
- **External reference catalogs:** AAVSO VSX and Gaia DR3;
- **Hackathon product:** a curated and crossmatched dataset prepared for the event.

Any scientific result should record:

- data-access date;
- source catalog paths or releases;
- sky coverage;
- crossmatch radius and neighbor policy;
- selected alert-history field;
- handling of duplicate historical measurements;
- VSX selection criteria;
- Gaia astrometric-quality criteria;
- period-search bounds;
- adopted extinction, metallicity, and distance calibration.

## Scientific cautions

- A VSX source, Gaia `source_id`, Rubin `diaSourceId`, and Rubin DIA object are different entities.
- Spatial proximity does not guarantee a correct physical association.
- VSX classifications and periods are heterogeneous.
- High-proper-motion sources may require epoch propagation.
- `prvDiaForcedSources` can contain measurements repeated across multiple alert packets.
- Alert forced-source fluxes are not automatically equivalent to calibrated total-flux light curves.
- Distance estimates require compatible photometric calibration, extinction, metallicity, and uncertainty propagation.
- Low signal-to-noise or non-positive Gaia parallaxes should not be inverted naively.

## Troubleshooting

### `ModuleNotFoundError: No module named 'lsdb'`

Confirm that the correct environment and Jupyter kernel are active:

```python
import sys
print(sys.executable)
```

The path should include `envs/lincc-rubin`.

### Gaia S3 or `storage_options` errors

Use the HTTPS Gaia path used in the notebooks:

```python
GAIA_PATH = "https://data.lsdb.io/hats/gaia_dr3/gaia/"
```

### `NestedFrame.to_parquet()` rejects `index=False`

Remove `index=False`, or use the `safe_to_parquet` helper supplied in the notebooks.

### `write_catalog()` fails while creating a summary or sky map

Keep these options disabled:

```python
create_summary=False
create_thumbnail=False
should_write_skymap=False
```

This does not remove the scientific catalog data.

## Contributing

Issues and pull requests are welcome for:

- portability fixes;
- clearer documentation;
- additional variable-star examples;
- improved uncertainty propagation;
- scientifically justified period–luminosity or period–Wesenheit implementations.

Please do not commit large data products, credentials, or private Drive links.

## Citation and acknowledgment

If you use these materials, acknowledge the relevant data providers and software projects, including Rubin Observatory, Gaia, AAVSO VSX, LINCC Frameworks, LSDB, HATS, and the scientific publications appropriate to the selected catalogs and calibrations.

A formal citation file can be added once the repository title, authorship, version, and preferred citation are finalized.
