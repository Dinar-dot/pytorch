from pathlib import Path
from typing import Any, Dict
import glob
import json

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def flatten_data(d: Dict[str, Any]) -> Dict[str, Any]:
    # Flatten the sccache stats data from a possibly nested dictionary to a flat
    # dictionary.  For example, the input:
    # {
    #     "cache": {
    #         "hit": 1,
    #         "miss": 2,
    #     },
    # }
    # will be transformed to:
    # {
    #     "cache_hit": 1,
    #     "cache_miss": 2,
    # }
    flat_data = {}
    for key, value in d.items():
        if isinstance(value, dict):
            for k, v in flatten_data(value).items():
                flat_data[f"{key}_{k}"] = v
        else:
            flat_data[key] = value
    return flat_data


def main() -> None:
    records = []
    for file in glob.glob(str(REPO_ROOT / "sccache-stats-*.json")):
        with open(file) as f:
            data = json.load(f)

            # I don't know what sccache info will be most useful yet, and the
            # sccache json has a decent number of keys, so just flatten the data
            # and store all of it
            records.append(
                {
                    "benchmark": {
                        "name": "sccache_stats",
                    },
                    "metric": {
                        "name": "sccache_stats",
                        "extra_info": flatten_data(data),
                    },
                }
            )
    with open(REPO_ROOT / "test" / "test-reports" / "sccache-stats.json", "w") as f:
        json.dump(records, f)


if __name__ == "__main__":
    main()
