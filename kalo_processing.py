import numpy as np
import soundfile as sf
import time
import os
import librosa
import argparse
import glob
import shutil
import re

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def create_output_folder(output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
        print(f"Output folder '{output_path}' created.")
    else:
        pass

def pad_audio_files(output_folder_path, chunk_size, original_sample_rate=44100):
    print("Starting padding process...")

    # Generate a list of all files in the output (after other changes) folder
    all_files = glob.glob(os.path.join(output_folder_path, '*.wav'))

    # Sort the files based on their numeric order
    all_files.sort(key=natural_sort_key)

    for file in all_files:
        # Determine the duration of the file
        print(f"Determining duration for file: {file}")
        data, sample_rate = sf.read(file)
        duration = len(data) / sample_rate * 1000  # Convert to ms

        # Calculate the amount of padding needed to match chunk_size
        padding_duration = chunk_size - duration
        padding_samples = int(padding_duration * sample_rate / 1000)

        # Split the padding equally for the start and end
        padding_samples_start = padding_samples // 2
        padding_samples_end = padding_samples - padding_samples_start

        # Create the padding arrays for the start and end
        padding_start = np.zeros((padding_samples_start, data.shape[1]), dtype=data.dtype)
        padding_end = np.zeros((padding_samples_end, data.shape[1]), dtype=data.dtype)

        # Concatenate the padding to the start and end of the audio data
        padded_data = np.concatenate((padding_start, data, padding_end), axis=0)

        # Write the padded data back to the file
        sf.write(file, padded_data, original_sample_rate)

        print(f"Padded '{file}' with {chunk_size}ms of silence.")

def rms(arr):
    return np.linalg.norm(arr) / np.sqrt(len(arr))

def find_quietest(arr, window_size, min_index=0):
    window = np.ones(window_size) / window_size
    rms_values = np.sqrt(np.convolve(np.square(arr), window, 'valid'))
    return np.argmin(rms_values[min_index:]) + min_index

global original_sample_rate

def split_audio(input_file, chunk_size, split_1, split_2, min_split, output_path, processing_sample_rate=22050, original_sample_rate=44100):
    data, _ = librosa.load(input_file, sr=processing_sample_rate, mono=True)
    data_original, _ = sf.read(input_file)
    print(f"Audio file '{input_file}' read successfully.")

    # Calculate window sizes in terms of number of samples
    chunk_samples = int(chunk_size/1000 * processing_sample_rate)
    split_1_samples = int(split_1/1000 * processing_sample_rate)
    split_2_samples = int(split_2/1000 * processing_sample_rate)
    min_split_samples = int(min_split/1000 * processing_sample_rate)

    piece_num = 1
    start_index = 0
    while start_index < len(data):
        sample_start_time = time.time()

        chunk_data = data[start_index:min(start_index + chunk_samples, len(data))]

        # If the remaining data is less than chunk_samples, save the remaining data as the last piece
        if len(chunk_data) < chunk_samples:
            output_file = f'{output_path}/{os.path.basename(os.path.splitext(input_file)[0])}SPLIT_{piece_num}.wav'
            start_index_original = int(start_index * original_sample_rate / processing_sample_rate)
            sf.write(output_file, data_original[start_index_original:], original_sample_rate)
            print(f"Remaining data saved to '{output_file}'.")
            break

        print(f"Processing chunk #{piece_num} starting at sample {start_index}.")

        min_index_100ms = max(0, min_split_samples - split_1_samples)
        quietest_100ms = find_quietest(chunk_data, split_1_samples, min_index_100ms)
        #print(f"Quietest 100ms period starts at sample {quietest_100ms}.")

        min_index_50ms = max(0, min_split_samples - quietest_100ms - split_2_samples)
        quietest_50ms_within_100ms = quietest_100ms + find_quietest(chunk_data[quietest_100ms:quietest_100ms+split_1_samples], split_2_samples, min_index_50ms)
        #print(f"Quietest 50ms period within the quietest 100ms period starts at sample {quietest_50ms_within_100ms}.")

        end_index = start_index + quietest_50ms_within_100ms + split_2_samples // 2

        output_file = f'{output_path}/{os.path.basename(os.path.splitext(input_file)[0])}SPLIT_{piece_num}.wav'
        start_index_original = int(start_index * original_sample_rate / processing_sample_rate)
        end_index_original = int(end_index * original_sample_rate / processing_sample_rate)
        sf.write(output_file, data_original[start_index_original:end_index_original], original_sample_rate)

        print(f"Piece #{piece_num} saved to '{output_file}'.")

        sample_time = time.time() - sample_start_time
        total_samples = piece_num
        total_time = sample_time * total_samples

        #print(f"Time taken for this sample: {sample_time:.6f} seconds")
        #print(f"Average sample creation length: {total_time / total_samples:.6f} seconds")

        start_index = end_index
        piece_num += 1

def process_files(input_folder_path, output_folder_path, chunk_size):
    extensions = ['.wav', '.flac', '.m4a', '.ogg', '.mp3']

    for extension in extensions:
        for input_file in glob.glob(os.path.join(input_folder_path, f'*{extension}')):
            split_1 = 250
            split_2 = 50
            min_split = 500
            split_audio(input_file, chunk_size, split_1, split_2, min_split, output_folder_path)

def merge_files(output_folder_path, chunk_size, original_sample_rate=44100):
    print("Starting merging process...")

    # Generate a list of all files in the output folder
    all_files = glob.glob(os.path.join(output_folder_path, '*.wav'))

    # Sort the files based on their names (not numerically)
    all_files.sort()

    i = 0
    while i < len(all_files) - 1:  # Ignore the last file
        file = all_files[i]

        # Determine the durations of the files
        print(f"Determining duration for file: {file}")
        data1, sample_rate1 = sf.read(file)
        duration1 = len(data1) / sample_rate1 * 1000  # Convert to ms

        # Initialize variables
        total_duration = duration1
        files_to_merge = [data1]
        merged_indexes = []  # Keep track of merged files' indexes

        j = i + 1

        # Loop through next files until total duration is close to chunk size
        while total_duration < chunk_size and j < len(all_files):
            next_file = all_files[j]
            print(f"Determining duration for file: {next_file}")
            data2, sample_rate2 = sf.read(next_file)
            duration2 = len(data2) / sample_rate2 * 1000  # Convert to ms

            # If merging this file would not exceed the chunk size, merge it
            if total_duration + duration2 <= chunk_size:
                print(f"Adding file {next_file} to merge list")

                # Handle mono/stereo channel differences
                if len(data1.shape) < len(data2.shape):
                    data1 = np.tile(data1[:, np.newaxis], [1, data2.shape[1]])
                elif len(data1.shape) > len(data2.shape):
                    data2 = np.tile(data2[:, np.newaxis], [1, data1.shape[1]])

                # Add the file to the merge list and update the total duration
                files_to_merge.append(data2)
                total_duration += duration2
                merged_indexes.append(j)
                j += 1
            else:
                # If this file would exceed the chunk size, skip it
                j += 1

        # Merge the files
        if len(files_to_merge) > 1:  # If there are files to merge
            print(f"Merging files from {file} to {all_files[j-1]}")
            merged_data = np.concatenate(files_to_merge, axis=0)

            # Write the merged data to the first file
            sf.write(file, merged_data, original_sample_rate)
            print(f"Merged files from '{file}' to '{all_files[j-1]}' into '{file}'.")

            # Delete the other files from the filesystem and the list
            for k in merged_indexes:
                os.remove(all_files[k])
            for index in sorted(merged_indexes, reverse=True):
                del all_files[index]

        # If no file was merged, increment i to try next file
        i += 1

if __name__ == "__main__":
    chunk_size = 3700
    original_sample_rate = 44100
    
    parser = argparse.ArgumentParser(description='Process audio files.')
    parser.add_argument('folder_path', type=str, help='Path to the output directory')

    args = parser.parse_args()

    output_folder_path = args.folder_path
    input_folder_path = os.path.dirname(output_folder_path)

    create_output_folder(output_folder_path)

    os.chdir(input_folder_path)

    process_files(input_folder_path, output_folder_path, chunk_size)

    merge_files(output_folder_path, chunk_size)

    pad_audio_files(output_folder_path, chunk_size)
