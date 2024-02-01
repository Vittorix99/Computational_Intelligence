from genetic import * 


if __name__ == "__main__":
    train = False
    if train:
        best_agent = evolution_strategy()
        np.save("genome_strategy.npy", best_agent.genome_strategy)
        np.save("genome_row.npy", best_agent.genome_row)
    else:
        genome_strategy = np.load("./Computational_Intelligence/lab2/genome_strategy.npy")
        genome_row = np.load("./Computational_Intelligence/lab2/genome_row.npy")
        genome = (genome_strategy, genome_row)
        best_agent = NimAgent(genome)

    nim = Nim(NUM_ROWS)

    total_win = 0
    for i in range(10):
        #print(f"First Moves Games {i+1}")
        nim.reset()
        winner , _, _=  nim.play1(adaptive, pure_random)
        #print(f"Winner: Player{winner}")
        if winner ==1:
            total_win += 1
    print("Adaptive vs Random")
    print("Random wins: " ,10-total_win)
    print("Adaptive wins: " ,total_win)
    print("===============================")

    total_win = 0
    for i in range (10):
        #print(f"Second Moves Games {i+1}")
        nim.reset()
        winner , _, _=  nim.play1(pure_random, adaptive)
        #print(f"Winner: Player{winner}")
        if winner ==2:
            total_win += 1
    print("Random vs Adaptive")
    print("Random wins: " , 10-total_win)
    print("Adaptive wins: " ,total_win)
    print("===============================")




    print("Gabriele vs Adaptive")
    total_win = 0
    for i in range(10):
        #print(f"First Moves Games {i+1}")
        nim.reset()
        winner , _, _=  nim.play1(adaptive, gabriele)
        #print(f"Winner: Player{winner}")
        if winner ==1:
            total_win += 1

    print("Adaptive vs Gabriele")
    print("Gabriele wins: " ,10 - total_win)
    print("Adaptive wins: " , total_win)
    print("===============================")

    total_win = 0
    for i in range (10):
        #print(f"Second Moves Games {i+1}")
        nim.reset()
        winner , _, _=  nim.play1(gabriele, adaptive)
        #print(f"Winner: Player{winner}")
        if winner ==2:
            total_win += 1
    print("Gabriele vs Adaptive")
    print("Gabriele wins: ",10 - total_win)
    print("Adaptive wins: ", total_win)
    print("===============================")





    total_win = 0
    for i in range(10):
        #print(f"First Moves Games {i+1}")
        nim.reset()
        winner , _, _=  nim.play1(adaptive, optimal)
        #print(f"Winner: Player{winner}")
        if winner ==1:
            total_win += 1
    print("Adaptive vs Optimal")
    print("Optimal wins: ",10 - total_win)
    print("Adaptive wins: ", total_win)
    print("===============================")

    
    


    total_win = 0
    for i in range (10):
        #print(f"Second Moves Games {i+1}")
        nim.reset()
        winner , _, _=  nim.play1(optimal, adaptive)
        #print(f"Winner: Player{winner}")
        if winner ==2:
            total_win += 1

    print("Optimal vs Adaptive")
    print("Optimal wins: ",10 - total_win)
    print("Adaptive wins: ", total_win)
    print("===============================")


    #print(f"Total win: {total_win}")









        