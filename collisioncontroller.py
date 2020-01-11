
def checkCollision(T):
    for i in range(len(T) - 1):
        for j in range(i + 1, len(T)):
            if T[i].ingombro.colliderect(T[j].visione):
                if T[j].direzione == 'destra' or T[j].direzione == 'sinistra':
                    T[j].speedx = 1
                    break
                elif T[j].direzione == 'su' or T[j].direzione == 'giù':
                    T[j].speedy = 1  
                    break 
            T[j].speedx = 2
            T[j].speedy = 2
    return 