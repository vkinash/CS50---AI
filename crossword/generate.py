import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # raise NotImplementedError
        for key in self.domains:
            domain = self.domains[key].copy()
            for var in self.domains[key]:
                if len(var) > key.length or len(var) < key.length:
                    domain.remove(var)
            self.domains.update({key: domain})

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # raise NotImplementedError
        if not self.crossword.overlaps[x, y]:
            return False

        overlap_x, overlap_y = self.crossword.overlaps[x, y]
        domain = self.domains[x].copy()
        overlap_y_symbols = {i[overlap_y] for i in self.domains[y]}
        for x_val in domain:
            if x_val[overlap_x] not in overlap_y_symbols:
                self.domains[x].remove(x_val)

        if len(domain) != len(self.domains[x]):
            return True
        return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # raise NotImplementedError
        if not arcs:
            queue = arcs
        else:
            queue = list()
            for i in self.domains:
                for j in self.domains:
                    if i != j and self.crossword.overlaps[i, j]:
                        queue.append((i, j))

        while queue:
            x, y = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for i in self.domains:
                    if x != i and y != y and self.crossword.overlaps[x, i]:
                        queue.insert(0, (self.domains[i], x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # raise NotImplementedError
        assignment_flag = False
        if len(self.domains) != len(assignment):
            return assignment_flag

        for val in assignment:
            if assignment[val]:
                assignment_flag = True

        return assignment_flag

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # raise NotImplementedError
        # if len(assignment) == 1:
        #     return True

        unq_val = set()
        for var_i in assignment:

            # every value is the correct length
            if var_i.length != len(assignment[var_i]):
                return False

            # there are no conflicts between neighboring variables.
            for var_neighbors in self.crossword.neighbors(var_i):
                if var_neighbors not in assignment:
                    continue

                overlap_var, overlap_neighbors = self.crossword.overlaps[var_i, var_neighbors]
                if assignment[var_i][overlap_var] != assignment[var_neighbors][overlap_neighbors]:
                    return False

            unq_val.add(assignment[var_i])

        # all values are distinct
        if len(unq_val) != len(assignment):
            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # raise NotImplementedError
        if not assignment:
            return self.domains[var]

        order_dict = {i: 0 for i in self.domains[var]}

        for v in self.domains:
            if v == var or v in assignment or not self.crossword.overlaps[var, v]:
                continue

            overlap_x, overlap_y = self.crossword.overlaps[var, v]

            for val in self.domains[var]:
                for n_val in self.domains[v]:
                    if val[overlap_x] == n_val[overlap_y]:
                        order_dict[val] += 1

        return sorted(order_dict, key=order_dict.get)[::-1]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # raise NotImplementedError
        variable = None
        max_var = len(self.domains[max(self.domains, key=lambda v: len(self.domains[v]))])
        var_list = list()
        for var in self.domains:
            if var not in assignment:
                if len(self.domains[var]) <= max_var:
                    var_list.append(var)

        if len(var_list) == 1:
            variable = var_list.pop()
            return variable
        elif len(var_list) == 0:
            return variable
        cnt_arcs = 0
        for var in var_list:
            if len(self.crossword.neighbors(var)) > cnt_arcs:
                cnt_arcs = len(self.crossword.neighbors(var))
                variable = var

        return variable

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result is not None:
                    return result
        return None


def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
