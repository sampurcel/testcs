# Detection-as-Code Sample for MSSP

This repository demonstrates how to manage CrowdStrike correlation rules using
an **MSSP** setup. Each customer has a separate rule file and workflow that
executes the `sync_detections.py` script with credentials stored in GitHub
Secrets.

## Structure

```
.
├── .github/workflows        # GitHub Actions workflows
├── rules                    # JSON rule definitions per customer
├── scripts                  # Synchronisation script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

The `scripts/sync_detections.py` script reads a JSON file of rule definitions
and submits them to the CrowdStrike API. When `falconpy` is not installed (for
example in local testing without internet access) the script will simply output
the rules it would submit.

## Usage

Each workflow uses different credentials and rule files. Add the corresponding
`FALCON_CLIENT_ID`, `FALCON_CLIENT_SECRET` and `FALCON_CID` secrets to your
GitHub repository or organisation for each tenant. The workflows can be run
manually or on a schedule to keep detection rules in sync.
