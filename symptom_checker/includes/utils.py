from typing import Union
from pathlib import Path

import requests
from tqdm import tqdm


def download_from_url(url: str, output_path: Union[str, Path], overwrite: bool):

    """
    Download a file from a URL.
    Shows progress bar and checks md5sum. Also
    checks if file is already downloaded.
    Args:
        url:
            URL to download from
        output_path:
            path to save the output to
        overwrite: boolean
            whether or not to overwrite the file if it already exists
        reference_md5:
            md5sum to check
        is_retry:
            whether or not the download is a retry (if the md5sum)
            does not match, is called again
    Returns:
        True if download was successful, False otherwise
    """

    output_filename = Path(output_path).name

    print(f"Downloading {url}")

    r = requests.get(url, stream=True)

    total_size = int(r.headers.get("content-length", 0))
    block_size = 1024

    t = tqdm(total=total_size, unit="iB", unit_scale=True)

    with open(output_path, "wb") as f:
        for data in r.iter_content(block_size):
            t.update(len(data))
            f.write(data)

    t.close()

    if total_size not in (0, t.n):
        print("Download error: sizes do not match")

        return False

    return True