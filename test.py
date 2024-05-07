import matplotlib.pyplot as plt

def test_bit_randomness(file_path):
    # Otwieramy plik i odczytujemy zawartość jako dane binarne
    with open(file_path, 'rb') as file:
        binary_data = file.read()

    # Konwertujemy dane binarne na listę intów
    integers = [int(byte) for byte in binary_data]

    # Tworzymy histogram
    plt.hist(integers, bins=range(256), edgecolor='black')
    plt.title('Histogram sekwencji bajtów')
    plt.xlabel('Wartość bajta')
    plt.ylabel('Liczba wystąpień')
    plt.show()

# Testujemy funkcję dla pliku random_sequence.bin
# test_bit_randomness('random_sequence.bin')
# test_bit_randomness('extractor_bites.bin')
test_bit_randomness('extractor_bites.bin')