import gdown
import zipfile

# output.zip 다운로드(현재 경로)
id = '1G09kwOycnNpf8lurt_iW9VqYBkKsOlfn'
output = 'output.zip'
gdown.download(id=id, output=output, quiet=False)

# output.zip 압축해제
output = zipfile.ZipFile('output.zip')
output.extractall()
output.close()