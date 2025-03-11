import random

#Disarankan untuk menjalakan program di Visual Studio Code agar UI lebih baik

class Node:
    def __init__(self, data):
        self.data = data
        self.player_positions = []  # save players name
        self.next = None
        self.jump = None

class Board:
    def __init__(self):
        self.head = None
        self.size = 0

    def add_board(self, size):
        self.size = size #save the board size
        self.head = Node(1)
        ptr = self.head
        for i in range(2, size * size + 1):
            new_node = Node(i)
            ptr.next = new_node
            ptr = ptr.next

    def box(self, data, player_positions, isStair, isSnake):
        padding = 8
        top = f"╭{'─' * padding}╮"
        middle = f"│ {data.center(padding - 2)} │"
        
        splitter = f"├{'─' * padding}┤"
        if isStair:
            player = f"│ 🪜 {player_positions.center(padding - 4)} │"
        elif isSnake:
            player = f"│ 🐍{player_positions.center(padding - 4)} │"
        else:
            player = f"│ {player_positions.center(padding - 2)} │"
        
        bottom = f"╰{'─' * padding}╯"
        return top, middle, splitter, player, bottom

    def display_board(self):
        ptr = self.head
        top, middle, splitter, player, bottom = "", "", "", "", ""

        while ptr:
            #check if there is a stair or a snake
            isStair = ptr.jump and ptr.data < ptr.jump.data
            isSnake = ptr.jump and ptr.data > ptr.jump.data
            
            boxes = self.box(str(ptr.data), ','.join(ptr.player_positions), isStair, isSnake)
            top += boxes[0] + " "
            middle += boxes[1] + " "
            splitter += boxes[2] + " "
            player += boxes[3] + " "
            bottom += boxes[4] + " "

            if ptr.data % self.size == 0:
                print(top)
                print(middle)
                print(splitter)
                print(player)
                print(bottom)
                top, middle, splitter, player, bottom = "", "", "", "", ""
            ptr = ptr.next
            
                
    def add_stair_snake(self, target, address):
        ptr = self.head
        target_node = None
        address_node = None
        while ptr:
            if ptr.data == target:
                target_node = ptr
            if ptr.data == address:
                address_node = ptr
            ptr = ptr.next
            
        if target_node and address_node:
            target_node.jump = address_node
        else:
            print(f"Error: target or address not found!")

        
board = Board() #board object


class Player:
    def __init__(self, name):
        self.name = name
        self.current_position = board.head
        self.prev_node = None
        self.step = 0
        self.maxboard = board.size * board.size

    def move(self, board):
        #dice
        roll_dice = random.randint(1,6)
        
        
        #Handle if dice is over flow from the board size
        target_position = self.current_position.data + self.step
        if target_position > self.maxboard:
            ulartangga.show_message(f'Dice {self.name} ({self.step}) overflow! still on position ({self.current_position.data})')
            self.step = roll_dice
            return False
        
        self.prev_node = self.current_position #save old node
        
        # delete jejak old player
        if self.prev_node and self.name in self.prev_node.player_positions:
            self.prev_node.player_positions.remove(self.name)

            
        
        # contiune to new position
        ptr = self.current_position
        ulartangga.show_message(f'{self.name} roll dice: ({self.step})')
        for _ in range(self.step):
            if ptr.next:
                ptr = ptr.next
        
        self.step = 0 #clear step
            
        #update player_positions
        if ptr.jump: #kalo ada tangga atau ular update ptr
            ulartangga.show_message(f'{self.name} jump from {ptr.data} to {ptr.jump.data}!')
            ptr = ptr.jump
            
        ptr.player_positions.append(self.name)
        self.current_position = ptr #update posisi terbaru
        
        #roll dice
        self.step = roll_dice 
        
        board.display_board() #display old the board
        
        #if the winner is found
        if self.current_position.data == self.maxboard:
            ulartangga.show_winner_message(f'🏆 We have the winner, Congratulation for {self.name}! 👏')
            return True
        return False

#controller game
class UlarTangga:
    players = []
    
    
    def show_winner_message(self, msg):
        top = '░█▀▀░█▀█░█▄█░█▀▀░░░█▀█░█░█░█▀▀░█▀▄'
        mid = '░█░█░█▀█░█░█░█▀▀░░░█░█░▀▄▀░█▀▀░█▀▄'
        bottom = '░▀▀▀░▀░▀░▀░▀░▀▀▀░░░▀▀▀░░▀░░▀▀▀░▀░▀'
        line_length = 55
        print(f"╭{'─'*line_length}╮")
        print(f"│ {''}{' ':<{line_length-2}} │")
        print(f"│ {top.center(line_length - 2)} │")
        print(f"│ {mid.center(line_length - 2)} │")
        print(f"│ {bottom.center(line_length - 2)} │")
        print(f"│ {''}{' ':<{line_length-2}} │")
        print(f"├{'─'*line_length}┤")
        print(f"│ {msg.center(line_length - 4)} │")
        print(f"╰{'─'*line_length}╯")
    
    def show_message(self, msg):
        lenght_msg = len(msg) + 2
        print(f"╭{'─'*lenght_msg}╮")
        print(f"│ {msg} │")
        print(f"╰{'─'*lenght_msg}╯")
    
    def menu(self):
        line_length = 60
        top = '░█░█░█░░░█▀█░█▀▄░░░▀█▀░█▀█░█▀█░█▀▀░█▀▀░█▀█'
        mid = '░█░█░█░░░█▀█░█▀▄░░░░█░░█▀█░█░█░█░█░█░█░█▀█'
        bottom = '░▀▀▀░▀▀▀░▀░▀░▀░▀░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀'
        submenu = '1. Start new Game', '2. About','3. Exit'
        message = 'Welcome to the Ular Tangga, play your luck,'
        message2 = 'and beat all your opponets to be the number one.'
        print(f"╭{'─'*line_length}╮")
        print(f"│ {''}{' ':<{line_length-2}} │")
        print(f"│ {top.center(line_length - 2)} │")
        print(f"│ {mid.center(line_length - 2)} │")
        print(f"│ {bottom.center(line_length - 2)} │")
        print(f"│ {''}{' ':<{line_length-2}} │")
        print(f"├{'─'*line_length}┤")
        print(f"│ {message.center(line_length - 2)} │")
        print(f"│ {message2.center(line_length - 2)} │")
        print(f"├{'─'*line_length}┤")
        for item in submenu:
            print(f"│ {item}{' ':<{line_length-len(item)-2}} │")
        print(f"╰{'─'*line_length}╯")
    
    def choose_board_menu(self):
        while True:
            line_length = 60
            top = '░█░█░█░░░█▀█░█▀▄░░░▀█▀░█▀█░█▀█░█▀▀░█▀▀░█▀█'
            mid = '░█░█░█░░░█▀█░█▀▄░░░░█░░█▀█░█░█░█░█░█░█░█▀█'
            bottom = '░▀▀▀░▀▀▀░▀░▀░▀░▀░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀'
            submenu = '1. Classic (10x10)', '2. Fast (8x8)','3. Long (12x12)', '4. Demo (5x5)'
            message = 'Please choose the board size to continue the game.'
            print(f"╭{'─'*line_length}╮")
            print(f"│ {''}{' ':<{line_length-2}} │")
            print(f"│ {top.center(line_length - 2)} │")
            print(f"│ {mid.center(line_length - 2)} │")
            print(f"│ {bottom.center(line_length - 2)} │")
            print(f"│ {''}{' ':<{line_length-2}} │")
            print(f"├{'─'*line_length}┤")
            print(f"│ {message.center(line_length - 2)} │")
            print(f"├{'─'*line_length}┤")
            for item in submenu:
                print(f"│ {item}{' ':<{line_length-len(item)-2}} │")
            print(f"╰{'─'*line_length}╯")
            try:
                option = int(input('Enter your size board: '))
                if option == 1:
                    board.add_board(10)
                    #stair
                    board.add_stair_snake(4,14)
                    board.add_stair_snake(9,31)
                    board.add_stair_snake(20,38)
                    board.add_stair_snake(28,84)
                    board.add_stair_snake(40,59)
                    #snake
                    board.add_stair_snake(87,74)
                    board.add_stair_snake(62,18)
                    board.add_stair_snake(48,26)
                    board.add_stair_snake(93,73)
                    board.add_stair_snake(99,78)
                elif option == 2:
                    board.add_board(8)
                    #stair
                    board.add_stair_snake(5,25)
                    board.add_stair_snake(13,46)
                    board.add_stair_snake(27,54)
                    #snake
                    board.add_stair_snake(60,41)
                    board.add_stair_snake(49,30)
                    board.add_stair_snake(38,19)
                elif option == 3:
                    board.add_board(12)
                    #stair
                    board.add_stair_snake(5,27)
                    board.add_stair_snake(17,45)
                    board.add_stair_snake(30,72)
                    board.add_stair_snake(48,91)
                    board.add_stair_snake(66,120)
                    #snake
                    board.add_stair_snake(140,101)
                    board.add_stair_snake(118,94)
                    board.add_stair_snake(97,64)
                    board.add_stair_snake(76,49)
                    board.add_stair_snake(53,29)
                elif option == 4:
                    board.add_board(5)
                    #stair
                    board.add_stair_snake(3,12)
                    board.add_stair_snake(8,20)
                    #snake
                    board.add_stair_snake(22,14)
                    board.add_stair_snake(18,6)
                break
            except ValueError:
                self.show_message('Invalid input, make sure you enter a number')
    
    def set_player_role_menu(self):
        while True:
            line_length = 60
            top = '░█░█░█░░░█▀█░█▀▄░░░▀█▀░█▀█░█▀█░█▀▀░█▀▀░█▀█'
            mid = '░█░█░█░░░█▀█░█▀▄░░░░█░░█▀█░█░█░█░█░█░█░█▀█'
            bottom = '░▀▀▀░▀▀▀░▀░▀░▀░▀░░░░▀░░▀░▀░▀░▀░▀▀▀░▀▀▀░▀░▀'
            message1 = "Let’s set up the game! Please specify how many"
            message2 = 'players will be playing in this game.'
            print(f"╭{'─'*line_length}╮")
            print(f"│ {''}{' ':<{line_length-2}} │")
            print(f"│ {top.center(line_length - 2)} │")
            print(f"│ {mid.center(line_length - 2)} │")
            print(f"│ {bottom.center(line_length - 2)} │")
            print(f"│ {''}{' ':<{line_length-2}} │")
            print(f"├{'─'*line_length}┤")
            print(f"│ {message1.center(line_length - 2)} │")
            print(f"│ {message2.center(line_length - 2)} │")
            print(f"╰{'─'*line_length}╯")
            try:
                num_players = int(input('Please include the number of players who will be playing: '))
                if  num_players >= 1 and num_players <=6:
                    for i in range (num_players):
                        self.players.append(Player(f'P{i+1}'))
                    break
                else:
                    self.show_message('Invalid player number, make sure the number range 1-6')
            except ValueError:
                self.show_message('Invalid input, make sure you enter a number')
                
    #clear all history game            
    def clear_game(self):
        board.head = None #hapus node
        self.players = [] #hapus players
        
    def play(self):
        self.choose_board_menu()
        self.set_player_role_menu()
        #playing the game
        winner = False
        while not winner:
            for player in self.players:
                option = input(f"Press Enter to roll the dice ({player.name})...")
                if player.move(board):
                    winner = True
                    break
                if option.lower() == 'exit':
                    self.show_message('Cacelled the Game.')
                    winner = True
                    break
        #clear all after game over
        self.clear_game()
        self.show_message('Old game has been deleted')
        
ulartangga = UlarTangga() #buat objek dari ular tangga

#Main Program
while True:
    ulartangga.menu()
    try:
        option = int(input('Enter your option: '))
        if option == 1:
            ulartangga.play()
        elif option == 2:
            ulartangga.show_message('This Game is made by Anugerah Gari')
        elif option == 3:
            break
    except ValueError:
        ulartangga.show_message('Invalid input, make sure you enter a number')