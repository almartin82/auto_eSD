import zipfile


def unzip(file='Access.zip'):
    """
    Unzips the eSD Access file.

    Args:
        file (str): full location (directory plus filename) of the Access download.

    Returns:
        bool: True if the file was unzipped without errors
    """
    zip_ref = zipfile.ZipFile(file, 'r')
    zip_ref.extractall('access_backup')
    zip_ref.close()
    print('Successfully unzipped file!')
    return True
