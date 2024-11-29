def compare_codes(guess:str, secret:str):
    correct_counter=0
    correctish_counter=0
    guess_list=list(guess)
    secret_list=list(secret)
    unmatched_guess=[]
    unmatched_secret=[]
    
    for i in range(4):
        if guess_list[i]==secret_list[i]:
            correct_counter+=1
        else:
            unmatched_guess.append(guess_list[i])
            unmatched_secret.append(secret_list[i])

    for i in unmatched_guess:
        if i in unmatched_secret:
            correctish_counter += 1
            unmatched_secret.remove(i)
    print(f"Total correct: {correct_counter}, Total Correctish: {correctish_counter}")
 
    return (correct_counter,correctish_counter)
compare_codes("RBYG", "RGBY")