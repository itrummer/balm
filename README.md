# BALM: Batch Analysis with Language Models

BALM makes processing batches of documents via large language models easy. Features include:
- Accessible user interface without coding.
- Support for zero-shot and few-shot learning.
- Easy profiling of models on the same task.
- Automatic result aggregation and visualization.

## Local Setup

The following installation instructions have been tested with Python 3.10 on Ubuntu Server 22.04.

1. Download this repository, e.g., by executing 
```
git clone https://github.com/itrummer/balm
```
2. Make sure that pip is installed:
```
pip --version
```
If you get an error message, install pip:
```
sudo apt-get update
sudo apt install python3-pip
```
3. Change into the `balm` directory and install requirements:
```
cd balm
sudo pip install -r requirements.txt
```

## Running BALM

From the `balm` directory, execute:
```
./start.sh
```
You should see the message `You can now view your Streamlit app in your browser.`, followed by a Network URL and an External URL. Enter the Network URL to access a local BALM installation and the External URL to access a remote BALM server. If using BALM remotely, make sure that port 8501 is reachable. E.g., when running BALM on an Amazon EC2 instance, change the Inbound Rules by adding a custom TCP rule for port 8501.

## Example: Analyzing Movie Reviews

We will introduce the BALM interface by an example scenario. You find the example data [here](https://drive.google.com/file/d/1pLtLcOSVsTjrMrHq27RzcYg8NdldV0CU/view?usp=sharing). It is a .csv file containing 100 movie reviews in the first column. You will use language models to map reviews to a sentiment (positive or negative) in the following.

