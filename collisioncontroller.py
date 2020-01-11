
def checkCollision(T):
    collide = None
    for i in range(len(T) - 1):
        for j in range(i + 1, len(T)):
            if T[i].visione.colliderect(T[j].ingombro):
                T[i].speedy = 0 
                T[i].speedx = 0
                collide = True 
            if not collide:              
                T[j].speedx = 2
                T[j].speedy = 2
                collide = False    
                               
            # if T[i].visione.colliderect(T[j].ingombro):
            #     T[i].speedy = 0
            #     T[i].speedx = 0            
        # T[j].speedx = 2
        # T[j].speedy = 2
    return 