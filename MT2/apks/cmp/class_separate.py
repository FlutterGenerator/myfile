import os

def main():
    print("ANTIK MODX TOOL")

    file_path = input("Please enter the path /> ")

    if not os.path.isfile(file_path):
        print("The file does not exist />")
        return

    try:
        with open(file_path, 'r') as input_file, open('Only_class.cs', 'w') as output_file:
            counter = 1
            for line in input_file:
                if 'public class' in line:
                    output_file.write(f"{counter}: {line}")
                    counter += 1
        
        print("Extraction complete. Check the 'output.txt' file for results.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()