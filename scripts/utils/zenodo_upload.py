#!/usr/bin/env python3
"""
Upload data to Zenodo using their REST API.
Requires: requests
Install: pip install requests
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from typing import Dict, Any
import requests
from tqdm import tqdm  # for progress bars

class ZenodoUploader:
    def __init__(self, sandbox: bool = False):
        """Initialize Zenodo API connection.
        
        Args:
            sandbox: Use sandbox.zenodo.org for testing
        """
        self.token = os.getenv('ZENODO_TOKEN')
        if not self.token:
            raise ValueError("Set ZENODO_TOKEN environment variable")
        
        # API endpoints
        self.base = "https://sandbox.zenodo.org" if sandbox else "https://zenodo.org"
        self.api = f"{self.base}/api"
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def create_deposit(self, metadata: Dict[str, Any]) -> int:
        """Create new deposit and return ID."""
        r = requests.post(
            f"{self.api}/deposit/depositions",
            json={},
            headers=self.headers
        )
        r.raise_for_status()
        deposition_id = r.json()['id']

        # Update metadata
        r = requests.put(
            f"{self.api}/deposit/depositions/{deposition_id}",
            data=json.dumps({'metadata': metadata}),
            headers={**self.headers, 'Content-Type': 'application/json'}
        )
        r.raise_for_status()
        return deposition_id

    def upload_file(self, deposition_id: int, filepath: Path) -> None:
        """Upload file to deposit with progress bar."""
        # Get bucket URL
        r = requests.get(
            f"{self.api}/deposit/depositions/{deposition_id}",
            headers=self.headers
        )
        r.raise_for_status()
        bucket_url = r.json()['links']['bucket']

        # Upload with progress bar
        filesize = filepath.stat().st_size
        with tqdm(total=filesize, unit='B', unit_scale=True) as pbar:
            with open(filepath, 'rb') as f:
                r = requests.put(
                    f"{bucket_url}/{filepath.name}",
                    data=FileWithCallback(f, pbar.update),
                    headers=self.headers
                )
        r.raise_for_status()

    def publish(self, deposition_id: int) -> Dict[str, Any]:
        """Publish deposit and return metadata."""
        r = requests.post(
            f"{self.api}/deposit/depositions/{deposition_id}/actions/publish",
            headers=self.headers
        )
        r.raise_for_status()
        return r.json()

class FileWithCallback:
    """Wrapper for file object to update progress bar."""
    def __init__(self, fd, callback):
        self.fd = fd
        self.callback = callback

    def read(self, size):
        chunk = self.fd.read(size)
        self.callback(len(chunk))
        return chunk

def calculate_checksums(filepath: Path) -> Dict[str, str]:
    """Calculate MD5 and SHA256 checksums."""
    md5 = hashlib.md5()
    sha256 = hashlib.sha256()
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            md5.update(chunk)
            sha256.update(chunk)
            
    return {
        'md5': md5.hexdigest(),
        'sha256': sha256.hexdigest()
    }

def main():
    parser = argparse.ArgumentParser(description='Upload data to Zenodo')
    parser.add_argument('files', nargs='+', help='Files to upload')
    parser.add_argument('--title', required=True, help='Dataset title')
    parser.add_argument('--description', required=True, help='Dataset description')
    parser.add_argument('--creators', required=True, help='Authors (LastName, FirstName;...)')
    parser.add_argument('--sandbox', action='store_true', help='Use sandbox.zenodo.org')
    args = parser.parse_args()

    # Prepare metadata
    metadata = {
        'title': args.title,
        'upload_type': 'dataset',
        'description': args.description,
        'creators': [
            {'name': name.strip()} 
            for name in args.creators.split(';')
        ],
        'access_right': 'open',
        'license': 'cc-by-4.0'
    }

    try:
        # Initialize uploader
        uploader = ZenodoUploader(sandbox=args.sandbox)
        
        # Create deposit
        print("Creating Zenodo deposit...")
        deposition_id = uploader.create_deposit(metadata)
        
        # Upload files
        print("Uploading files...")
        for filepath in args.files:
            path = Path(filepath)
            if not path.is_file():
                print(f"Skipping {path}: not a file")
                continue
                
            print(f"\nUploading {path}")
            print("Calculating checksums...")
            checksums = calculate_checksums(path)
            print(f"MD5: {checksums['md5']}")
            print(f"SHA256: {checksums['sha256']}")
            
            uploader.upload_file(deposition_id, path)
        
        # Publish
        print("\nPublishing deposit...")
        result = uploader.publish(deposition_id)
        
        print(f"\nSuccess! Dataset published:")
        print(f"DOI: {result['doi']}")
        print(f"URL: {result['links']['html']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 