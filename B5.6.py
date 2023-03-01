print()
print("Добро пожаловать в игру крестики-нолики!")
print('Игровое поле ниже')
print()
print("*" * 15)
print()

board = [[" "] * 3 for i in range(3)]

def playing_field():
    print(f'  | 0 | 1 | 2 |')
    print('-' * 15)
    for i in range(3):
        line = " | ".join(board[i])
        print(f'{i} | {line} |')
        print('-' * 15)
    print()


def make_move():
    while True:
        player_answer = input('Куда поставим свой ход? Назовите координаты: ').split()
        print()

        if len(player_answer) != 2:
            print('Ввести нужно две координаты!')
            print()
            continue

        a, b = player_answer

        if not a.isdigit() or not b.isdigit():
            print('Некорректный ввод! Вы ввели не цифры. Попытайтесь еще раз')
            print()
            continue

        a, b = int(a), int(b)

        if 0 > a or a > 2 or 0 > b or b > 2:
            print('Неверный диапазон')
            print()
            continue

        if board[a][b] != " ":
            print('Клетка уже занята! Выберите другую.')
            print()
            continue

        return a, b

def check_win():
    win_coord = (((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                 ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                 ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0)))
    for coord in win_coord:
        x = coord[0]
        y = coord[1]
        z = coord[2]

        if board[x[0]][x[1]] == board[y[0]][y[1]] == board[z[0]][z[1]] != ' ':
            print(f'Выиграл {board[x[0]][x[1]]}! Поздравляем!')
            return True
    return False


def main():
    counter = 0

    while True:

        playing_field()
        if counter % 2 == 1:
            print("Ходит крестик")
            print()
        else:
            print("Ходит нолик")
            print()

        a, b = make_move()

        if counter % 2 == 1:
            board[a][b] = 'X'
        else:
            board[a][b] = '0'

        counter += 1

        if check_win():
            break

        if counter == 9:
            print('Ничья!')
            break


main()
