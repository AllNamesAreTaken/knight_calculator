#   A lot of these loops could be functions, but I just needed it to visualize how knights move

class VBoard:
    knight_moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    def __init__(self, src):
        #   [col][row]
        self.board = [[-1]*8 for col in range(8)]
        self.src = src
        self.src_col = src % 8
        self.src_row = src//8
        self.max_hops = 0
        self.board[self.src_col][self.src_row] = 0
        self.solve([(self.src_col, self.src_row)])

    def __str__(self):
        to_ret = "src: {0} -> ({1}, {2})\n//|".format(self.src, self.src_col, self.src_row)
        for col in range(0, 8):
            to_ret += "C{0}|".format(col)
        to_ret += '\n'
        for row in range(0, 8):
            to_ret += "-"*26 + '\n'
            to_ret += "R{0} ".format(row)
            for col in range(0, 8):
                to_ret += "{0:02d} ".format(self.board[col][row])
            to_ret += '\n'
        to_ret += "max_hops: {0}".format(self.max_hops)
        return to_ret

    #   This is the brute force method, not the solution to the problem
    def solve(self, start_spots, hops=1):
        if len(start_spots) == 0:
            return
        next_spots = []
        for c_col, c_row in start_spots:
            for m_col, m_row in VBoard.knight_moves:
                next_col = c_col + m_col
                next_row = c_row + m_row
                if 0 <= next_col < 8 and 0 <= next_row < 8 and self.board[next_col][next_row] == -1:
                    self.board[next_col][next_row] = hops
                    next_spots.append((next_col, next_row))
                    self.max_hops = max(self.max_hops, hops)
        self.solve(next_spots, hops=hops+1)

    def fill_rel(self, rel_board):
        #   Middle is 7,7
        for col in range(0, 8):
            for row in range(0, 8):
                rel_col = col - self.src_col
                rel_row = row - self.src_row
                dest_col = 7 + rel_col
                dest_row = 7 + rel_row
                rel_board[dest_col][dest_row].append((self.board[col][row], self.src_col, self.src_row))

    def known_answer(self, dst):
        dst_col = dst % 8
        dst_row = dst//8
        #print(self.board[dst_col][dst_row])
        return self.board[dst_col][dst_row]


#   [col][row]
test_boards = [[None]*8 for col in range(8)]
rel_board = [[[] for row in range(15)] for col in range(15)]

def solution(src, dst):
    print("sorry pal, make you're own solution")
    print("look at the data and come up with your own method")
    return 0

def check_answer():
    incorrect_answers = 0
    for test_src in range(64):
        for test_dst in range(64):
            test_src_col = test_src % 8
            test_src_row = test_src//8
            src_board = test_boards[test_src_col][test_src_row]
            #tdc = test_dst % 8
            #tdr = test_dst//8
            known_answer = src_board.known_answer(test_dst)
            cal_answer = solution(test_src, test_dst)
            if known_answer != cal_answer:
                incorrect_answers += 1
                print("Failure #{0} src: {1} dst: {2}, known: {3} cal: {4}".format(incorrect_answers,
                                                                                   test_src,
                                                                                   test_dst,
                                                                                   known_answer,
                                                                                   cal_answer))
    if incorrect_answers == 0:
        print("Failures: 0 - NICE")
    else:
        print("Failures: {0}".format(incorrect_answers))


if __name__ == '__main__':
    cur_start = 0
    max_hops = 0
    min_hops = 7
    for col in range(0, 8):
        for row in range(0, 8):
            src_val = col + (row*8)
            new_board = VBoard(src_val)
            max_hops = max(max_hops, new_board.max_hops)
            min_hops = min(min_hops, new_board.max_hops)
            print("start: {0:02d},{1:02d}".format(col, row))
            print(new_board)
            test_boards[col][row] = new_board
            new_board.fill_rel(rel_board)


    to_print = "// |"
    for col in range(15):
        to_print += "C{0:02d}|".format(col-7)
    to_print += '\n'
    for row in range(15):
        to_print += "-" * 64 + '\n'
        to_print += "R{0:02d} ".format(row-7)
        for col in range(15):
            temp_dict = {}
            for count, or_col, or_row in rel_board[col][row]:
                temp_dict[count] = True
            if len(temp_dict) > 1:
                to_print += "  {0:01d} ".format(len(temp_dict))
            else:
                to_print += "  * "
        to_print += '\n'
    #to_print += "max_hops: {0}".format(self.max_hops)
    print(to_print)

    to_print = "// |"
    for col in range(15):
        to_print += "C{0:02d}|".format(col-7)
    to_print += '\n'
    for row in range(15):
        to_print += "-" * 64 + '\n'
        to_print += "R{0:02d} ".format(row-7)
        for col in range(15):
            temp_dict = {}
            com_val = -1
            for count, or_col, or_row in rel_board[col][row]:
                temp_dict[count] = True
                com_val = count
            if len(temp_dict) > 1:
                to_print += "  * "
            else:
                to_print += "  {0:01d} ".format(com_val)
        to_print += '\n'
    #to_print += "max_hops: {0}".format(self.max_hops)
    print(to_print)


    print("debug")
    cur_input = input("Coordinates:")
    while cur_input != 'exit':
        if 'test' == cur_input:
            check_answer()
        elif ':' in cur_input:
            spl_input = cur_input.split(":")
            if len(spl_input) == 2 and spl_input[0].isdigit() and spl_input[1].isdigit():
                col_input = int(spl_input[0])
                row_input = int(spl_input[1])
                print(test_boards[col_input][row_input])
        elif 'max' == cur_input:
            print("max: {0}".format(max_hops))
        elif 'min' == cur_input:
            print("min: {0}".format(min_hops))
        elif 'q' == cur_input:
            num_spots = 0
            to_print = "// |"
            for col in range(15):
                to_print += "C{0:02d}|".format(col - 7)
            to_print += '\n'
            for row in range(15):
                to_print += "-" * 64 + '\n'
                to_print += "R{0:02d} ".format(row - 7)
                for col in range(15):
                    temp_dict = {}
                    com_val = 20
                    for count, or_col, or_row in rel_board[col][row]:
                        temp_dict[count] = True
                        com_val = min(com_val, count)
                    if row >= col >= 7 and com_val > -1:
                        print(row)
                        if len(temp_dict) == 1:
                            to_print += "  \033[92m{0:01d}\033[0m ".format(com_val)
                            num_spots += 1
                        else:
                            to_print += "  \033[93m{0:01d}\033[0m ".format(com_val)
                            num_spots += 1
                    else:
                        to_print += "  * "
                to_print += '\n'
            # to_print += "max_hops: {0}".format(self.max_hops)
            print(to_print)
            print("Number of spots: {0}".format(num_spots))
        elif cur_input.isdigit():
            target_val = int(cur_input)
            num_spots = 0
            to_print = "// |"
            for col in range(15):
                to_print += "C{0:02d}|".format(col - 7)
            to_print += '\n'
            for row in range(15):
                to_print += "-" * 64 + '\n'
                to_print += "R{0:02d} ".format(row - 7)
                for col in range(15):
                    temp_dict = {}
                    com_val = -1
                    for count, or_col, or_row in rel_board[col][row]:
                        temp_dict[count] = True
                        com_val = count
                    if len(temp_dict) == 1 and com_val == target_val:
                        to_print += "  \033[92m{0:01d}\033[0m ".format(com_val)
                        num_spots += 1
                    elif target_val in temp_dict:
                        to_print += "  \033[93m{0:01d}\033[0m ".format(target_val)
                        num_spots += 1
                    else:
                        to_print += "  * "
                to_print += '\n'
            # to_print += "max_hops: {0}".format(self.max_hops)
            print(to_print)
            print("Number of spots: {0}".format(num_spots))
        cur_input = input("Coordinates:")
