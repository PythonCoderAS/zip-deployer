# zip-deployer
Deploy a zip file if it matches a given key.

## Setup

First, make a file `config.py` in the root directory with the following contents (replace as needed):

```python
secret_key = "my-secret"
export_to = "/directory"
new_url = "https://my-staging-%s.example.com"
```

The secret key should be a unique and _not shared_ key as this allows anyone to write arbitrary files to your server and have the browser return them.

The new_url has one modifier (specified with `%s`): The name of the zip file without the extension.

Once the file is made, run `docker build -t zip-deployer .` to build the image.

## Usage

To run the server, run `docker run -p 8000:8000 -v /out/real-directory:/directory zip-deployer`.
