import os

# Get the input values
text = os.environ["INPUT_INPUT_TEXT"]
numOfRepeats = int(os.environ["INPUT_NUM_OF_REPEATS"])

outputText = ""
for i in range(numOfRepeats):
    outputText += text

# Set the output value
with open(os.environ["GITHUB_OUTPUT"], "a") as f:
    f.write(f"output_text={outputText}\n")
