
# Hugo Erlandsson 2024      
# Python 3.12.8


# Instruktion: kör programmet i terminalen. Välj att skapa nycklar. Kopiera endast siffrorna i arrayen i botten till höger, detta är den privata nyckeln. Välj "kryptera" och följ instruktion i terminalen. Kopiera det krypterade meddelandet från tmp.txt eller mata in "kopiera" för att göra det automatiskt. Kör programmet igen, välj att dekryptera, följ instruktion. Det avkrypterade meddelandet skrivs ut i terminalen. 


import numpy as np
import binascii


q = 127   # storleken på en ring av tal. begränsning i vilka tal som får vara med
n = 8     
N = int(1.1 * n * np.log(q))

def lattice_keys():

    t = np.random.randint(0, high=q/2, size=n)
    s = np.concatenate([np.ones(1, dtype=np.int32), t])   # hemlig/privat nyckel

    A = np.random.randint(0, high=q/2, size=(N, n))    # slumpad N x n matris med tal från ringen av q tal
    e = np.round(np.random.randn(N)).astype(np.int32) % q    # error/noise vector    "fel-vektor"?
    b = ((np.dot(A, t) + e).reshape(-1, 1)) % q     # del av offentlig nyckel som beror på dn privata nyckeln

    P = np.hstack([b, -A])   # offentlig nyckel

    return P, s


def lattice_one_bit(plaintext, P):  

    r = np.random.randint(0, 2, N)   # slumpar en vektor att modifiera den offentliga nyckeln med, så att kryptering av samma meddelande/sekvens ändå ger olika ciphertext

    m = np.concatenate([np.array([plaintext]), np.zeros(n, dtype=np.int32)]) 

    c = (np.dot(P.T, r) + (np.floor(q / 2) * m)).astype(np.int32) % q

    return c

def lattice_decrypt_one_bit(c, s):
    plaintext = round((np.dot(c, s) % q) * (2 / q)) % 2    # ytterst låg risk att krypteras till fel värde, sannolikhen är i storleksordningen 2^(-150)

    return plaintext


def lattice_string(plaintext, P):
    plaintext_binary = bin(int.from_bytes(plaintext.encode(), 'big'))   # binär form

    cipher = []
    i = 2   # skippar index 0 och 1 som är 0 och b och inte ska krypteras
    while i < len(plaintext_binary):
        cipher.append(lattice_one_bit(int(plaintext_binary[i]),P))  # konkatenera ciphertext med varje krypterad bit
        i += 1

    return cipher

def lattice_string_decrypt(ciphertext, s):
    decrypted_binary = "0b"   # lägger till 0b så python förstår att det är ett binärt meddelande och kan konvertera till ascii(bokstäver mm.)
    for c in ciphertext:   # plockar varje krypterad bit ur cipher_binary, avkrypterar den och konkatenerar ihop varje avkrypterat bit
        
        decrypted_binary += str(lattice_decrypt_one_bit(np.array(c), s))

    
    n = int(decrypted_binary, 2)  # bas 2, binärt
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()  # // dividerar med avrundning neråt

def string_to_list_of_arrays(str):
    
    listan = str.replace("array(","")
    listan = listan.replace(", dtype=int32), ", ", dtype=int32)")
    listan = listan.split(", dtype=int32)")

    listan.pop(-1)
    i = 0
    while i < len(listan):
        listan[i] = listan[i].replace("[", "").replace("]","").replace(" ","").split(",")
        j = 0
        while j < len(listan[i]):
            listan[i][j] = int(listan[i][j])
            j += 1
        listan[i] = np.array(listan[i])
        i += 1
    return listan
    
def string_to_array(str):
    tmp = str.split(", ")
    i = 0
    while i < len(tmp):
        tmp[i] = int(tmp[i])
        i += 1
    
    return np.array(tmp)

def run():
    
    fortsätt = True
    while fortsätt:
        print("Hej, vad vill du göra?  skapa nycklar (n)   kryptera(k)   dekryptera(d)   avbryt(a)")
        choice = input()
        if choice == "n":
            print("En uppsättning nycklar skrivs ut, offentlig sen privat")
            keys = lattice_keys()
            key = keys[0] 
            print(keys)
            
                    
        elif choice == "k":
            print("skriv in ett meddelande att kryptera")
            msg = input()

            print("\n", "ditt krypterade meddelande skrivs ut i tmp.txt. Starta om programmet manuellt", "\n")
            f = open("tmp.txt", "w")
            f.write(str(lattice_string(msg, key)))
            f.close
            return
        elif choice == "d":
            print("skriv in ett krypterat meddelande")
            tmp_input = input()
            if tmp_input == "kopiera":
                f = open("tmp.txt", "r")
                cipher = string_to_list_of_arrays(f.read())
            else:
                cipher = string_to_list_of_arrays(input())

            print("skriv in den rätta privata nyckeln")
            secret_key = string_to_array(input())

            print("\n", "Ditt avkryperade meddelande:", "\n", lattice_string_decrypt(cipher, secret_key), "\n")
            return

        else:
            print("programmet avslutades")
            fortsätt = False

run()



# Delar hämtade från artikeln "Let’s code Lattice-Based Encryption: The post-quantum encryption." av Phiphat Chomchit:
# https://medium.com/@phiphatchomchit/lets-code-lattice-based-encryption-the-post-quantum-encryption-6ce613a9e05a
