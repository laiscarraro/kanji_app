# External libs
import zipfile, io, requests

def extract_zip(url, max=100):
    '''
    Extract .zip subtitle files.
    '''
    r = requests.get(url, stream=True).content

    try:
        input_zip = zipfile.ZipFile(io.BytesIO(r))
    except zipfile.BadZipFile:
        return None, None
    
    filenames = input_zip.namelist()

    try:
        files = [input_zip.read(name).decode('utf8') for name in filenames[:min(max, len(filenames))]]
    except UnicodeDecodeError:
        return None, None

    return filenames, files