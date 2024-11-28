import matplotlib.pyplot as plt

frequencies = []
db_values = []

with open("dftop", "r", encoding="utf-8", errors="replace") as file:
    for line in file:
        try:
            if "Hz" in line and "dB" in line:
                freq, db = line.strip().split(": ")
                frequencies.append(float(freq.split(" ")[0]))
                db_value = db.replace(" dB", "")
                db_values.append(float(db_value))
            else:
                print(f"Skipping malformed line: {line.strip()}")
        except ValueError as e:
            print(f"Skipping malformed line: {line.strip()} - Error: {e}")


print(f"Number of frequency data points: {len(frequencies)}")
print(f"Number of dB data points: {len(db_values)}")

if len(frequencies) == len(db_values) and len(frequencies) > 0:
    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, db_values, label="Power Spectrum (dB)")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Amplitude (dB)")
    plt.title("Frequency Spectrum")
    plt.grid(True)
    plt.legend()
    plt.show()
else:
    print("Error: No valid data to plot or mismatch between frequency and dB data lengths.")

