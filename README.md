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

We will introduce the BALM interface by an example scenario. You find the example data [here](https://drive.google.com/file/d/1pLtLcOSVsTjrMrHq27RzcYg8NdldV0CU/view?usp=sharing). It is a .csv file containing 100 movie reviews in the first column. We will use language models to map reviews to a sentiment (positive or negative) in the following. This example uses language models by OpenAI and requires a corresponding account (see [here](https://platform.openai.com/signup)).

1. Open the BALM interface in your Web browser (this example was tested on Google Chrome but most browsers will work).
2. Click on the `Credentials` box. Copy your OpenAI API key into the corresponding field (see [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)).
3. Click on the `Models` box. Leave the default (1) for the number of models. E.g., select the gpt-3.5-turbo model.
4. Enter a task description in the prompt field. For instance:
```
Is the sentiment positive (Yes/No)?
```
5. Optionally, specify examples to increase output quality (few-shot learning). Click on the `Examples` box, choose the number of examples, then enter example input and output. E.g.:
```
Example input: This movie was really bad.
Example output: No
```
6. Select CSV for the input type (the default), then click on `Browse files` and select the input file you previously downloaded.
7. Movie reviews are stored in the first column, therefore use 0 (default) for the column index (we count starting from zero).
8. Optionally, restrict the number of reviews to process by clicking on the `Limit rows` checkbox and setting a maximal number.
9. Click on the `Process Data` button to start processing.

You will see results in the result table as they become available from the language model. After processing all input, BALM automatically generates several aggregate statistics. Click on the `Output Distribution` box to obtain a visualization, showing how often specific outputs were produced by the language model. The `Model Agreement` box is only interesting if multiple models are applied to the same data (see the following section). Finally, you can download results as .csv file by clicking on the `Download Results` button. Note that this will erase the current results and reset the interface.
