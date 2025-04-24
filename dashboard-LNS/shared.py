from pathlib import Path

import pandas as pd

app_dir = Path(__file__).parent
tips = pd.read_csv(app_dir /www/ "LNS_openalex_full_metadata_REV2.csv")
