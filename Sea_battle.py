from random import randint

class Exceptions(Exception):
    pass

class BoardOutException(Exceptions):
    def __str__(self):
        return 'Вы ввели неверный диапазон! Корабль вышел за границы поля.'

class DotIsOccupied(Exceptions):
    def __str__(self):
        return 'Клетка уже занята! Выберите другую.'

class BoardWrongShipException(Exceptions):
    pass


class Dot():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot - ({self.x}, {self.y})'

class Ship():
    def __init__(self, length, bow, orientation):
        self.length = length
        self.bow = bow
        self.orientation = orientation
        self.hp = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            dot_x = self.bow.x
            dot_y = self.bow.y

            if self.orientation == 0:  # горизонтальное направление
                dot_x += i
            elif self.orientation == 1:  # вертикальное направление
                dot_y += i

            ship_dots.append(Dot(dot_x, dot_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board():
    def __init__(self, size=6, hid=False):
        self.size = size
        self.list_of_ships = []
        self.hid = hid
        self.live_ships = 7

        self.field = [[" O "] * size for _ in range(size)]

        self.busy_dot = []

    def __str__(self):
        board_ = ''
        board_ += '  | 1 | 2 | 3 | 4 | 5 | 6 |'
        for i, row in enumerate(self.field):
            board_ += f'\n{i + 1} |' + '|'.join(row) + '|'

        if self.hid:
            board_ = board_.replace('■', 'O')

        return board_


    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb=False):
        near = [
            (-1, 1), (0, 1), (1, 1),
            (-1, 0), (0, 0), (1, 0),
            (-1, -1), (0, -1), (1, -1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                course = Dot(d.x + dx, d.y + dy)
                if not(self.out(course)) and course not in self.busy_dot:
                    if verb:
                        self.field[course.x][course.y] = ' . '
                    self.busy_dot.append(course)

    def add_ship(self, ship):

        for d in ship.dots:
            if self.out(d) or d in self.busy_dot:
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = ' ■ '
            self.busy_dot.append(d)

        self.list_of_ships.append(ship)
        self.contour(ship)

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy_dot:
            raise DotIsOccupied()

        self.busy_dot.append(d)

        for ship in self.list_of_ships:
            if ship.shooten(d):
                ship.hp -= 1
                self.field[d.x][d.y] = ' X '
                if ship.hp == 0:
                    self.live_ships -= 1
                    self.contour(ship, verb=True)
                    print('Корабль был уничтожен!')
                    return False
                else:
                    print('Корабль был ранен!')
                    return True

        self.field[d.x][d.y] = ' . '
        print('Мимо!')
        return False

    def begin_game(self):
        self.busy_dot = []


class Player():
    def __init__(self, own_board, rival_board):
        self.own_board = own_board
        self.rival_board = rival_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.rival_board.shot(target)
                return repeat
            except Exceptions as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d


class User(Player):
    def ask(self):
        while True:
            player_answer = input('Куда поставим свой ход? Назовите координаты: ').split()
            print()

            if len(player_answer) != 2:
                print('Ввести нужно две координаты!')
                print()
                continue

            x, y = player_answer

            if not x.isdigit() or not y.isdigit():
                print('Некорректный ввод! Вы ввели не цифры. Попытайтесь еще раз')
                print()
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)

class Game():
    def __init__(self, size=6):
        self.size = size
        player_ = self.random_board()
        ai_ = self.random_board()
        ai_.hid = True

        self.ai = AI(ai_, player_)
        self.us = User(player_, ai_)

    def create_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        try_ = 0
        for l in lens:
            while True:
                try_ += 1
                if try_ > 1000:
                    return None
                ship = Ship(l, Dot(randint(0, self.size), randint(0, self.size)), randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin_game()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.create_board()
        return board

    def show(self):
        ai_board = str(self.ai.own_board)
        our_board = str(self.us.own_board)
        for x, y in zip(our_board.split('\n'), ai_board.split('\n')):
            print(x, " ", y)


    def greet(self):
        print()
        print('          ДОБРО ПОЖАЛОВАТЬ В ИГРУ "МОРСКОЙ БОЙ"!')
        print()
        print('  Правила ввода:\n'
              '1. Вводить можно только числа \n'
              '2. Вводить числа можно только в диапазоне от 1 до 6 \n'
              '3. x - номер строки \n'
              '4. y - номер столбца')
        print()
        print('                  Надеюсь Вам понравится!')
        print()
        print('*' * 57)

    def loop(self):
        num = 0
        while True:
            print()
            print("     Доска пользователя:", "           ", "Доска компьютера:")
            print(Game.show(self))
            print("-" * 57)

            if num % 2 == 0:
                print('Ходит пользователь!')
                repeat = self.us.move()
            else:
                print('Ходит компьютер!')
                repeat = self.ai.move()
            if repeat:
                num -= 0

            if self.ai.own_board.live_ships == 0:
                print('-' * 20)
                print('Пользователь выиграл!!! Поздравляем!')
                break

            if self.us.own_board.live_ships == 0:
                print('-' * 20)
                print('Компьютер выиграл!!! Попытайтесь в следующий раз!')
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()


a = Game()
a.start()


