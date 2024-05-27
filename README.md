# audio-trimmer

Trims the length of MP4 files that have prolonged silence or low audio at the end.

## Requirements

- Python 3.x
- moviepy
- pydub

## Installation

1. Install Python 3.x from the official website if you don't have it installed.
2. Install the required third-party libraries using pip:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Open your terminal or command prompt.
2. Navigate to the directory containing `trimmer.py`.
3. Run the script with the following command:

    ```sh
    python audio_trimmer.py <directory> [<append_str>]
    ```

    - `<directory>`: The path to the directory containing your MP4 files.
    - `[<append_str>]`: An optional string to append to the trimmed file names. Defaults to an empty string if not provided.

### Example

To process all MP4 files in the `videos` directory and append `-trimmed` to the filenames of the trimmed videos:

```sh
python audio_trimmer.py /path/to/videos -trimmed
```

The trimmed videos will be saved in a subdirectory called `trimmed_videos` within the specified directory.

## Notes

This was a really quick script I wrote in 20 minutes so I could be lazy and not have to manually trim videos with long silences at the end. Feel free to modify it to suit your needs.

- The script analyzes audio in chunks and trims the video when it detects 1.5 seconds of continuous silence below a threshold of -50 dBFS.
- Ensure you have `ffmpeg` installed and properly configured, as `moviepy` relies on it for video processing.

For further customization, you can modify the `silence_threshold` and `chunk_size` parameters within the script.
