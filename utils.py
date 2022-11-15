# External libs
import zipfile, io

def extract_zip(r, max=100):
    '''
    Extract .zip subtitle files.
    '''
    input_zip = zipfile.ZipFile(io.BytesIO(r.content))
    files = input_zip.namelist()
    return [input_zip.read(name).decode('utf8') for name in files[:min(max, len(files))]]
