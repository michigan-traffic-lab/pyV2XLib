# pyV2XLib

## Introduction

This is an open-source SDSM encoder/decoder API, built upon the [pycrate](https://github.com/P1sec/pycrate) framework (a Python library designed for compiling ASN1 files). This encoder/decoder API will enable seamless integration of external perception systems with RSUs for transmitting encoded SDSMs that comply with [SAE J2735](https://www.sae.org/standards/content/j2735set_202309/) and [SAE J3224](https://www.sae.org/standards/content/j3224_202208/). Users can effortlessly populate the SDSM data structure with an object list generated by the perception system and apply an appropriate header to precede the payload. The decoder is also supported with this repo.

Features:
- Encode the object list from the perception system into SDSM and validate its value.
- SDSM payload with an appropriate header. 
- Decode SDSM and generate the object list as output.

Code Structure:
```
pyV2XLib
|__ example
|____ SDSM_decoder.py
|____ SDSM_encoder.py
|__ pycrate_sdsm
|____ __init__.py
|____ SDSMDecoder.py
|____ SDSMEncoder.py
|__ setup.py
```

## Installation
1. Create conda environment

```
conda create -n sdsm python=3.8
conda activate sdsm
```

2. Install [pycrate](https://github.com/P1sec/pycrate) package

```bash
pip3 install pycrate
```

3. Clone this repo.

```bash
git clone https://github.com/michigan-traffic-lab/pyV2XLib.git
cd pyV2XLib
```

4. Download ASN.1 files

Download [SAE J2735 ASN.1 files](https://www.sae.org/standards/content/j2735asn_202309/) and [SAE J3224 ASN.1 file](https://www.sae.org/standards/content/j3224_202208/).

Once all ASN.1 files are prepared, place all files into one folder. The final folder structure is shown below:

```
ASN_1_file_folder
|__ J2735_ASN_1_file.asn
|__ ...
|__ J3224_ASN_1_file.asn
|__ ...
```

5. Compile ASN.1 files

Compile all ASN.1 files by using the following command:

```bash
pycrate_asn1compile.py -i path/to/ASN_1/files -o ./pycrate_sdsm/SDSM -j
```

Then ```./pycrate_sdsm/SDSM.json``` and ```./pycrate_sdsm/SDSM.py``` will be generated.

6. Install this package.

```bash
pip install .
```

## Usage
There are two examples (```./example/SDSM_encoder.py``` and ```./example/SDSM_decoder.py```) show how to use the SDSM encoder and decoder.

1. Encoder

All you need to do is to input all the information into the function ```sdsm_encoder()```. The input list of the encoder contains all the variables in SDSM. The definition and valid range of each variable are provided in ```./example/SDSM_encoder.py```. Please find more details in [SAE J2735](https://www.sae.org/standards/content/j2735set_202309/) and [SAE J3224](https://www.sae.org/standards/content/j3224_202208/).

Below is a concise example demonstrating how to utilize the function:
```
hex_sdsm = sdsm_encoder(
    msgCnt=0,
    sourceID="test",
    ...
)
```

The output of the encoder is the SDSM in hex format.

2. Decoder

To decode the SDSM, please input the SDSM into the function ```sdsm_decoder()```. The input of the decoder is the same as the output of the encoder.

Below is a concise example demonstrating how to utilize the function:

```
output = sdsm_decoder("00292b7f303030303001ec35a4edd26b49d6d1ffffffff00802c800f6cae4a002e13440001800000009014014140")
```

The output of the decoder is a dictionary, whose structure is the same as the SDSM structure defined in ASN.1 files. The keys are the varibles' names.

## Additional inforamtion

1. I cannot find the ASN.1 file for J3224

Please note that for J3224, the ASN.1 file is in the standard content. You will want to copy and paste it into a separate file.

2. There is an error when compiling the ASN.1 files

There may be some garbled characters in J2735 ASN.1 files that you will want to delete them.

3. After installing pycrate, ```pycrate_asn1compile.py``` cannot be recognized as a valid command

If this happens, you might want to find the file in the folder and use the following command to compile:

```bash
python3 path/to/anaconda/envs/sdsm/bin/pycrate_asn1compile.py -i path/to/ASN_1/files -o ./pycrate_sdsm/SDSM -j
```

Please note that the location of this file may be different under different operation systems.

4. Can I generate encoder and decoder for the other standard messages?

Sure. If you want to do this, first, you will want to download the ASN.1 files you need. Then compile the files by following step 4. Finally, develop the code that can convert the information into correct format so that the compiled files can encode and decode the message. That's why we need ```./pycrate_sdsm/SDSMEncoder.py``` and ```./pycrate_sdsm/SDSMDecoder.py``` in this repo and of course, you need to develop your own msg encoder and decoder.

5. Do I have to input all the information into the encoder every time?

No. Some of them are mandatory, while others are optional. Please find the description for this in ```./pycrate_sdsm/SDSMEncoder.py```.

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project

2. Create your Feature Branch (git checkout -b feature/AmazingFeature)

3. Commit your Changes (git commit -m 'Add some AmazingFeature')

4. Push to the Branch (git push origin feature/AmazingFeature)

5. Open a Pull Request

## License

Distributed under the MIT License.

## Developers
Tinghan Wang (tinghanw@umich.edu)

Rusheng Zhang (rushengz@umich.edu)

## Acknowledgement

The authors would like to thank the Federal Highway Administration (FHWA) at the U.S. DOT for the support. 

## Contact
Henry Liu (henryliu@umich.edu)
