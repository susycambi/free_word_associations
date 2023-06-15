import argparse
import speech_recognition as sr
from os import path
from pydub import AudioSegment
import os
from typing import List, Tuple

EXT = '.wav'

# Create the argument parser
parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', '-i', required=True, help='Input folder where to find .wav files')
parser.add_argument('--output_folder', '-o', required=True, help='Output folder where to write .txt files')
args = parser.parse_args()

# Access the value of the input and output 'folder' arguments
input_folder = args.input_folder
output_folder = args.output_folder
# this is for saving purposes
head_tail = os.path.split(input_folder)
word_name = head_tail[1]

print('Reading recordings under:', input_folder)

# FUNCTIONS

# `transcribe_recording` is the MAIN function here, which takes a .wav audio file and uses
# speech recognition with google API and returns the transcribed text

def transcribe_recording(path_to_audio: str) -> str:
    """
    Receives the path to a .wav file and returns the words, in french, from this file
    """
    # use the audio file as the audio source                                         
    r = sr.Recognizer()
    with sr.AudioFile(path_to_audio) as source:
        audio = r.record(source)  # read the entire audio file                  

    try:
        print("Google API: " + file + ":   " + r.recognize_google(audio, language = "fr-FR"))
        return r.recognize_google(audio, language = "fr-FR")

    except Exception as e:
        print(f'Error while transcripting: {e}')

# `save_words` is a function that takes as input a sentence of several words (the output of transcribe_recording) and 
# that writes / saves each of these words into a .txt file with a new line (\n) between each word (to facilitate copy-pasting)

def save_words(words: str, file_name: str):
    """
    """
    # specify path to output file
    output_path = args.output_folder + '/' + file_name.replace(EXT, '_words.txt')
    # add new line \n
    output = words.replace(' ', '\n')

    try:
        with open(output_path, "w") as output_file:
            # writing output into output file
            output_file.write(output)    
  
    except:
        print(f"  Error while to {output_path}")
        print("This is probably because the output folder does not exist.")
        print("Try creating it with `mkdir NAME_OF_FOLDER` \n")

# `save_all_subjects` is a function to save all the transcripts for ONE word (of all subjects) into the same .txt file
# this may be useful to avoid having to open all the .txt files

def save_all_subjects(all_subjects: List[Tuple[str, str]], output_path: str): # all_subjects will be a list of file names + their transcriptions
    output = ""
    for file, words in all_subjects:
        output += "\n\nNEW FILE: " + file + "\n"
        output += words.replace(' ', '\n')
    with open(output_path, "w") as output_file:
        output_file.write(output)     



# LET'S RUN
# get the files, function that takes the folder and returns the files in that folder
files = os.listdir(input_folder)

all_subjects = [] # empty list
for file in files:
    path = input_folder + '/' + file
    if file.endswith(EXT): # to make sure the file is in the right extension
        print(f"Processing {file}") 
        words = transcribe_recording(path)
        if words:
            all_subjects.append((file, words)) # to be able to use the function save_all_words
            save_words(words, file)
    print("Finished. Files writen under: ", args.output_folder)

save_all_subjects(all_subjects, output_folder + "/" + word_name + "_all_subjects.txt") # saves the transcripts of all subjects for one word