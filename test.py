import matplotlib.pyplot as plt

def test_bit_randomness(file_path):
    # Otwieramy plik i czytamy zawartość
    with open(file_path, 'r') as file:
        data = file.read()

    # Konwertujemy sekwencję bitów na listę intów
    bits = [int(bit) for bit in data if bit in ['0', '1']]

    # Tworzymy listę bajtów, grupując bity co 8
    bytes_list = [bits[i:i+8] for i in range(0, len(bits), 8)]

    # Konwertujemy każdy bajt na liczbę całkowitą
    integers = [int(''.join(map(str, byte)), 2) for byte in bytes_list]

    # Tworzymy histogram
    plt.hist(integers, bins=range(256), edgecolor='black')
    plt.title('Histogram sekwencji bajtów')
    plt.xlabel('Wartość bajta')
    plt.ylabel('Liczba wystąpień')
    plt.show()

# Testujemy funkcję dla pliku random_sequence.txt
test_bit_randomness('random_sequence.txt')
