# Operator for checking file size 
class Operator:
    def __init__(self, curr_file, target_size, operator):
        self.curr_file = curr_file
        self.target_size = target_size
        self.operator = operator

    def check(self):
        operator_mapping = self.get_operator_map()
        return operator_mapping[self.operator]

    def check_greater(self):
        return self.curr_file.get_size() > self.target_size
    
    def get_operator_map(self):
        return {
            ">": self.check_greater()
        }



if __name__ == '__main__':
    curr_file = "Anthony.txt"
    target_size = 5
    operator = ">"
    operator = Operator(curr_file, target_size, operator)
    operator.check()
    
