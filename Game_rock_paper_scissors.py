#import module for choose an option of array options
import random

print('|==== Welcome to the game rock, paper o scissors ====|')
print('|==== Choose the best option to beat the computer ===|')


#array for anwers PC
options = ['rock', 'paper', 'scissors']
#Pc choose an option
answer_pc = random.choice(options)

#User enter an option
answer_user = input('Enter you option: ')

#convert user response to lowercase
answer_user = answer_user.lower()

#If the answer of user in array options, run game
if answer_user in options:
    #Print answers of user and PC
    print('\n           |=====================|')
    print(f'You anwers: >>> {answer_user} vs {answer_pc} <<< :answer PC')
    print('           |=====================|')

    #All the options of Tie
    if answer_user == 'rock' and answer_pc == 'rock' or answer_user == 'paper' and answer_pc == 'paper' or answer_user == 'scissors' and answer_pc == 'scissors':
        
        print('               >>>> Tie <<<<')

    #All the options of lost
    elif answer_user == 'rock' and answer_pc == 'paper' or answer_user == 'paper' and answer_pc == 'scissors' or answer_user == 'scissors' and answer_pc == 'rock':
        print('             >>>> You lost <<<<')

    #All the options of win
    elif answer_user == 'rock' and answer_pc == 'scissors' or answer_user == 'paper' and answer_pc == 'rock' or answer_user == 'scissors' and answer_pc == 'paper':
        print('             >>>> You win ! <<<<')

    #Rules of game:
    print('\nRules of game:\n')
    print('Rock wins against scissors')

    print('Scissors win against paper')

    print('Paper wins against rock')
        
else:
    #Print for the user if write an options that not be found in array options
    print('Sorry, wrong answer, try again run code and write: rock, paper or scissors')