**FWA_transcriber.py** takes a folder of .wav files as input and returns their transcribed .txt files (one per subject) as well as one overall .txt. file for the cue/word with all subjects' transcripts

Before launching the FWA_transcriber.py script, you should have a folder for each word/cue, containing all the subjects' .wav files.
NB: you need to create an output folder beforehand, and provide input and output folders as arguments

The output can then be stored and copied into a dataframe.

Before running the code, specify where to find `ffmpeg` with the following command: 

```bash
export PATH=$PATH:~/ffmpeg/bin
```

Run the code with the command: 

```bash
python3 FWA_transcriber.py -i input folder -o output folder
```

**test_preproc_french_words.py** takes as input ToT_transcripts.csv, does pre-processing and text cleaning, tokenization, lemmatization, and returns (here as example) the file words-n-stuff.csv

**extract_counts.py** computes counts for the free associations, organizes the responses into collections, and pivots the results into a dataframe that might be easier to work with. The output files are both results.csv and pivoted_results.csv


