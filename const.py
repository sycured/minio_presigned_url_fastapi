"""Constants needed by the documentation."""

download_responses = {
    307: {'description': 'redirect to the file using presigned url'},
    404: {'description': 'bucket or file not found'},
}

upload_responses = {
    200: {'description': 'return presigned url to upload the file'},
    404: {'description': 'bucket not found'}
}

tags_metadata = [
    {
        'name': 'download',
        'description': 'Return presigned url to download the specified file.'
    },
    {
        'name': 'upload',
        'description': 'Return presigned url to upload the specified file.'
    }
]
