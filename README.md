# pyV2XLib

## Introduction

Features:
- Encode object list into sensor data sharing message (SDSM) and check if the value is valid.

Code Structure:
```
pyV2XLib
|__example
|____SDSM_decoder.py
|____SDSM_encoder.py
|__pycrate_sdsm
|____ __init__.py
|____SDSMDecoder.py
|____SDSMEncoder.py
|__setup.py
```

## Installation
1. Install [pycrate](https://github.com/P1sec/pycrate) package

```bash
pip3 install pycrate
```

2. Clone this repo.

```bash
git clone https://github.com/michigan-traffic-lab/pyV2XLib.git
cd pyV2XLib
```

3. Download ASN.1 files

Download [SAE J2735](https://www.sae.org/standards/content/j2735asn_202309/) and [SAE J3224](https://www.sae.org/standards/content/j3224_202208/) ASN.1 files.

Once all ASN.1 files are prepared, place all files into one folder. And the final folder structure is shown below:

```
ASN_1_file_folder
|__ J2735_ASN_1_file.asn
|__ ...
|__ J3224_ASN_1_file.asn
|__ ...
```

4. Compile ASN.1 files

Compile all ASN.1 files by using the follwing command:

```bash
pycrate_asn1compile.py -i path/to/ASN_1/files -o ./pycrate_sdsm/SDSM -j
```

Then ```./pycrate_sdsm/SDSM.json``` and ```./pycrate_sdsm/SDSM.py``` will be generated.

5. Install this package.

```bash
python3 setup.py install
```

## Usage
There are two examples (```./example/SDSM_encoder.py``` and ```./example/SDSM_decoder.py```) that can show you how to use the SDSM encoder and decoder.

1. Encoder

All you need to do is to input all the information into the function ```sdsm_encoder()```. The input list of the encoder contains all the variables in SDSM. Please find the definitions of them in [SAE J2735](https://www.sae.org/standards/content/j2735set_202309/) and [SAE J3224](https://www.sae.org/standards/content/j3224_202208/).

The output of the encoder is the SDSM in hex format.

2. Decoder

To decode the SDSM, please input the SDSM into the function ```sdsm_decoder()```. The input of the decoder is the same as the output of the encoder.

The output of the decoder is a dictionary, whose structure is the same as the SDSM structure defined in ASN.1 files. The keys are the varibles' names.

## Common issues

1. I connot find the ASN.1 file for J3224

Please note that for J3224, the ASN.1 file is in the standard content. You will want to copy and paste it into a seperate files.

2. There is an error when compiling the ASN.1 files

There are may some garbled characters in J2735 ASN.1 files that you will want to delete them.

3. After installing pycrate, ```pycrate_asn1compile.py``` cannot be recognized as a valid command

If this happens, you will want to find the file in the folder and use the following command to compile:

```bash
python3 path/to/anaconda/env/Scripts/pycrate_asn1compile.py -i path/to/ASN_1/files -o ./pycrate_sdsm/SDSM -j
```

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project

2. Create your Feature Branch (git checkout -b feature/AmazingFeature)

3. Commit your Changes (git commit -m 'Add some AmazingFeature')

4. Push to the Branch (git push origin feature/AmazingFeature)

5. Open a Pull Request

## License

Distributed under the MIT License.

## Developers
Tinghan Wang (tinghanw@umich.edu)

## Contact
Henry Liu (henryliu@umich.edu)
