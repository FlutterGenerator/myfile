#!/usr/bin/env python3

import re
import binascii
import argparse
import os
import sys

class FlutterWorkflowGenerator:
    def __init__(self, file_path, version_mapping):
        self.file_path = file_path
        self.version_mapping = version_mapping

    def read_file_content(self):
        try:
            with open(self.file_path, 'rb') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: The file '{self.file_path}' was not found. Please check the file path and try again.")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied to read the file '{self.file_path}'. Please check your file permissions.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            sys.exit(1)

    def convert_to_hex(self, content):
        return binascii.hexlify(content).decode()

    def extract_version_code(self, hex_string):
        pattern = re.compile(r'5c2200(.*?)2028737461626c6529')
        matches = pattern.findall(hex_string)
        return matches

    def get_flutter_sdk_version(self, byte_string):
        return self.version_mapping.get(byte_string.strip(), "Unknown version")

    def create_workflow_content(self, flutter_sdk_version):
        return f"""
name: Flutter Build

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up JDK
        uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          flutter-version: '{flutter_sdk_version}'

      - name: Print Flutter version
        run: flutter --version

      - name: Create and set up Flutter project
        run: |
          flutter create flutter_so
          cd flutter_so
          flutter pub get

      - name: Build APK for arm64 and armeabi-v7a
        run: |
          cd flutter_so
          flutter build apk --release --target-platform android-arm,android-arm64

      - name: Upload libflutter.so for arm64
        uses: actions/upload-artifact@v4
        with:
          name: libflutter_so_arm64
          path: flutter_so/build/app/intermediates/merged_native_libs/release/out/lib/arm64-v8a/libflutter.so

      - name: Upload libflutter.so for armeabi-v7a
        uses: actions/upload-artifact@v4
        with:
          name: libflutter_so_armeabi_v7a
          path: flutter_so/build/app/intermediates/merged_native_libs/release/out/lib/armeabi-v7a/libflutter.so
"""

    def save_workflow_file(self, content, flutter_sdk_version):
        file_name = f'flutter-build-{flutter_sdk_version}.yml'
        try:
            with open(file_name, 'w') as workflow_file:
                workflow_file.write(content)
            full_path = os.path.abspath(file_name)
            print(f"\nWorkflow file for Flutter SDK version {flutter_sdk_version} created as \n{full_path}")
        except IOError as e:
            print(f"Error: Unable to write to file '{file_name}'. {e}")
            sys.exit(1)

    def process(self):
        content = self.read_file_content()
        hex_string = self.convert_to_hex(content)
        version_codes = self.extract_version_code(hex_string)

        if version_codes:
            for match in version_codes:
                byte_string = binascii.unhexlify(match).decode('utf-8', errors='replace').strip()
                flutter_sdk_version = self.get_flutter_sdk_version(byte_string)
                if flutter_sdk_version != "Unknown version":
                    workflow_content = self.create_workflow_content(flutter_sdk_version)
                    self.save_workflow_file(workflow_content, flutter_sdk_version)
                else:
                    print(f"Warning: Unrecognized Flutter SDK version code: {byte_string}")
        else:
            print("No version code found in the file.")

def main():
    parser = argparse.ArgumentParser(description='Extract Flutter SDK version and create a GitHub Actions workflow file.')
    parser.add_argument('file_path', type=str, help='Path to the libflutter.so file')
    args = parser.parse_args()

    file_path = args.file_path

    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' does not exist. Please provide a valid file path.")
        sys.exit(1)

    version_mapping = {
    "3.6.0": "3.27.1",  # New version
    "3.6.0": "3.27.0",  # New version
    "3.5.4": "3.24.5",  # New version
    "3.5.4": "3.24.4",  # New version
    "3.5.3": "3.24.3",  # New version
    "3.5.2": "3.24.2",  # New version
    "3.5.1": "3.24.1",  # New version
    "3.5.0": "3.24.0",  # Existing version
    "3.4.4": "3.22.3", 
    "3.4.3": "3.22.2", 
    "3.4.1": "3.22.1", 
    "3.4.0": "3.22.0",
    "3.3.4": "3.19.6", 
    "3.3.3": "3.19.5", 
    "3.3.2": "3.19.4", 
    "3.3.1": "3.19.3",
    "3.3.0": "3.19.2", 
    "3.2.6": "3.16.9", 
    "3.2.5": "3.16.8", 
    "3.2.4": "3.16.7",
    "3.2.3": "3.16.6", 
    "3.2.2": "3.16.2", 
    "3.2.1": "3.16.1", 
    "3.2.0": "3.16.0",
    "3.1.5": "3.13.9", 
    "3.1.4": "3.13.8", 
    "3.1.3": "3.13.7", 
    "3.1.2": "3.13.5",
    "3.1.1": "3.13.3", 
    "3.1.0": "3.13.2", 
    "3.0.6": "3.10.6", 
    "3.0.5": "3.10.5",
    "3.0.3": "3.10.4", 
    "3.0.2": "3.10.2", 
    "3.0.1": "3.10.1", 
    "3.0.0": "3.10.0",
    "2.19.6": "3.7.12", 
    "2.19.5": "3.7.8", 
    "2.19.4": "3.7.7", 
    "2.19.3": "3.7.6",
    "2.19.2": "3.7.5", 
    "2.19.1": "3.7.1", 
    "2.19.0": "3.7.0", 
    "2.18.6": "3.3.10",
    "2.18.5": "3.3.9", 
    "2.18.4": "3.3.7", 
    "2.18.2": "3.3.6", 
    "2.18.1": "3.3.2",
    "2.18.0": "3.3.1", 
    "2.17.6": "3.0.5", 
    "2.17.5": "3.0.4", 
    "2.17.3": "3.0.2",
    "2.17.1": "3.0.1", 
    "2.17.0": "3.0.0", 
    "2.16.2": "2.10.5", 
    "2.16.1": "2.10.3",
    "2.16.0": "2.10.0", 
    "2.15.1": "2.8.1", 
    "2.15.0": "2.8.0", 
    "2.14.4": "2.5.3",
    "2.14.3": "2.5.2", 
    "2.14.2": "2.5.1", 
    "2.14.0": "2.5.0", 
    "2.13.4": "2.2.3",
    "2.13.3": "2.2.2", 
    "2.13.1": "2.2.1", 
    "2.13.0": "2.2.0", 
    "2.12.3": "2.0.6",
    "2.12.2": "2.0.4", 
    "2.12.1": "2.0.2", 
    "2.12.0": "2.0.1"
}

    extractor = FlutterWorkflowGenerator(file_path, version_mapping)
    extractor.process()

if __name__ == "__main__":
    main()
