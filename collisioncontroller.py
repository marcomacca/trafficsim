
def checkCollision(T):
    for i in range(len(T) - 1):
        for j in range(i + 1, len(T)):
            if T[i].ingombro.colliderect(T[j].ingombro):
                T[i].speedx = 0
                T[i].speedy = 0
                T[j].speedx = 0
                T[j].speedy = 0
                # return 1
    return 