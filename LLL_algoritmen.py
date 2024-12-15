import numpy as np

def gram_schmidt(B):
    n = B.shape[0]
    m = B.shape[1]
    B_reducerad = np.zeros((n, m))
    my = np.zeros((n, n)) 
    #my är en konstant som representerar projektionen och används 
    #för att förenkla beräkningarna i koden

    for i in range(n):
        B_reducerad[i] = B[i]
        for j in range(i):
            my[i, j] = np.dot(B[i], B_reducerad[j]) / np.dot(B_reducerad[j], B_reducerad[j])
            B_reducerad[i] -= my[i, j] * B_reducerad[j]

    return B_reducerad, my

def lovasz_villkor(B_reducerad, my, i, delta = 0.75):
    #Kontrollerar lovász-villkoret för den ortogonaliserade basen 
    vänster = delta * np.dot(B_reducerad[i], B_reducerad[i])
    höger = np.dot(B_reducerad[i + 1], B_reducerad[i + 1]) + my[i + 1, i]**2 * np.dot(B_reducerad[i], B_reducerad[i])
    return vänster <= höger

def LLL_algoritm(B, delta=0.75):
    
    n = B.shape[0]
    B_reducerad, my = gram_schmidt(B)

    k = 1
    while k < n:
        #Utför gram Schmidts ortogonaliseringsmetod
        for j in range(k - 1, -1, -1):
            if abs(my[k, j]) > 0.5:
                B[k] -= round(my[k, j]) * B[j]
                B_reducerad, my = gram_schmidt(B)

        #Kontrollerar lovász-villkoret för den reducerade basen och 
        #byter plats på basvektorerna utefter behov
        if not lovasz_villkor(B_reducerad, my, k - 1, delta):

            B[[k, k - 1]] = B[[k - 1, k]]
            B_reducerad, my = gram_schmidt(B)
            k = max(k - 1, 1)
        else:
            k += 1

    return B

def closest_vector(B, c):
    #Löser CVP-problemet med hjälp av en reducerade basen i LLL-algoritmen
    # Reducera basen först
    B_reduced = LLL_algoritm(B)

    # Projicerar punkten c på det reducerade gitteret
    B_inv = np.linalg.pinv(B_reduced)
    koefficienter = np.dot(B_inv, c)

    # Approximerar närmaste heltalsvektor
    koefficienter_avrundade = np.round(koefficienter)
    x = np.dot(B_reduced.T, koefficienter_avrundade)

    return x

# Exempel på en bas och en punkt:
B = np.array([[3, 2], [1, 2]], dtype=float)  #<-- Basen
c = np.array([2.1, 3.4])  #<-- Punkten som ska approximeras

# Hitta närmevektorn
x = closest_vector(B, c)

print("Den reducerade basen är:")
print(LLL_algoritm(B))
print("En närmevektor x till krypteringsproblemet är:")
print(x)
