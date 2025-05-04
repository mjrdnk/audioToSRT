# MacOS desktop app, converter of audio files into .srt files.

## Usage:

### Install dependencies
```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```


### Run app locally:
```bash
python setup.py py2app -A
./dist/Audio\ to\ SRT.app/Contents/MacOS/Audio\ to\ SRT
```

#### For production .dmg file generation check official docs of [py2app](http://py2app.readthedocs.io/)
