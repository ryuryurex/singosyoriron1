#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sndfile.h>

#define SAMPLE_RATE 44100
#define N 1024

void compute_dft(const char *input_filename, const char *output_filename) {

    SF_INFO sfinfo;
    SNDFILE *infile = sf_open(input_filename, SFM_READ, &sfinfo);
    if (!infile) {
        printf("Error: Could not open input file.\n");
        return;
    }

    float *data = (float*)malloc(N * sizeof(float));
    if (!data) {
        printf("Error: Memory allocation failed.\n");
        sf_close(infile);
        return;
    }

    sf_count_t frames_read = sf_readf_float(infile, data, N);
    if (frames_read < N) {
        printf("Error: Could not read enough frames (only %ld frames read)\n", frames_read);
        free(data);
        sf_close(infile);
        return;
    }

    FILE *outfile = fopen(output_filename, "w");
    if (!outfile) {
        printf("Error: Unable to open output file for writing.\n");
        free(data);
        sf_close(infile);
        return;
    }

    for (int k = 0; k < N / 2 + 1; k++) {
        double real = 0.0;
        double imag = 0.0;

        for (int n = 0; n < N; n++) {
            double angle = -2.0 * M_PI * k * n / N;
            real += data[n] * cos(angle);
            imag += data[n] * sin(angle);
        }

        double power = real * real + imag * imag;
        power = (power < 1e-10) ? 1e-10 : power;

        double db = 10 * log10(power);

        double frequency = (double)k * SAMPLE_RATE / N;

        fprintf(outfile, "%f Hz: %f dB\n", frequency, db);
    }

    fclose(outfile);
    free(data);
    sf_close(infile);

    printf("DFT and analysis completed successfully.\n");
}

int main() {
    compute_dft("aiueo.wav", "dftop");
    return 0;
}

