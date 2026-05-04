import os, subprocess, sys

sdcpp = "sdcpp/sd-cli"

inputs = []
for entry in os.scandir("."):
    if entry.name.endswith(".safetensors"):
        inputs.append(entry.name)

TYPES = [
    "f16",
    "f32",
    "q8_0",
    "q5_0",
    "q5_1", 
    "q4_0", 
    "q4_1",
    "q4_K",
    "q3_K",
    "q2_K"
]

if __name__ == '__main__':
    os.makedirs("output", exist_ok=True)

    if sys.platform.startswith("linux"):
        sdcpp = "sdcpp/l/sd-cli"
        subprocess.Popen(["chmod", "700", sdcpp], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', text=True)

    while True:

        available = ""
        for i, m in enumerate(inputs):
            available += f"{i}. {m} \n"
        try: r = int(input(f"\nChoose the INPUT Model: (0 = Defualt) \n\n{available} \n\n>> "))
        except: r = 0
        inputModel = inputs[r]

        available = ""
        for i, m in enumerate(TYPES):
            available += f"{i}. {m} \n"
        try: r = int(input(f"\nChoose the QUANT: (0 = Defualt) \n\n{available} \n\n>> "))
        except: r = 0
        outtype = TYPES[r]
        
        cmd = [
            sdcpp, 
            '-M', 'convert',
            '-m', inputModel,
            "-o", f"output/{inputModel}".replace(".safetensors", f"-{outtype}.gguf"),
            "-v",
            "--type", outtype
        ]

        print("\n" + " ".join(cmd))

        if input("\nWould you like to run the command as a subprocess? (Y/n) \n\n>> ").lower() == 'n':
            continue
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd='.', text=True)

        for line in process.stdout:
            print(line, end='') 

        process.wait()

        input("\n\n-- Process Ended --")