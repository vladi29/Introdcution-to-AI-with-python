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
                        w, h = draw.textsize(letters[i][j], font=font)
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
        
        for var in self.crossword.variables:
            SecDomain = self.domains[var].copy()
            for word in SecDomain:
                if var.length != len(word):
                    self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        if y not in self.crossword.neighbors(x): 
            return False
        if self.crossword.overlaps[x,y] == None:
            return False
        else:
            Revise = False
            i, j = self.crossword.overlaps[x,y]
            XDomain = self.domains[x].copy()
            for xword in XDomain:
                remove = True
                for yword in self.domains[y]:
                    if xword[i] == yword[j]:
                        remove = False
                if remove:
                    self.domains[x].remove(xword)
                    Revise = True
            return Revise


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs == None:
            arcs = list()
            for X in self.crossword.variables:
                for Y in self.crossword.variables:
                    if Y in self.crossword.neighbors(X) and Y != X:
                        arcs.append((X,Y))
        while arcs:
            x, y = arcs.pop()
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False 
                for z in self.crossword.neighbors(x) - self.domains[y]:
                    arcs.append((z,x))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.crossword.variables:
            if var in assignment:
                if assignment[var] == None:
                    return False
            else:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        keys = assignment.keys()
        set_words = set()

        #Distinct Values
        for var in keys:
            if assignment[var] not in set_words:
                set_words.add(assignment[var])
            else:
                return False

        #Unary Constraint
        for var in keys:
            if var.length != len(assignment[var]):
                return False
        
        #No conflicts between variables
        for var1 in keys:
            for var2 in keys:
                if var1!=var2 and var2 in self.crossword.neighbors(var1): #and self.crossword.overlaps[var1, var2]!=None
                    i, j = self.crossword.overlaps[var1, var2]
                    if assignment[var1][i] != assignment[var2][j]:
                        return False
        
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        list1 = list()
        DomainValues = list()
        for value in self.domains[var]:
            n = 0
            for neighbor in self.crossword.neighbors(var) - set(assignment):
                i, j = self.crossword.overlaps[var, neighbor]    
                for value1 in self.domains[neighbor]:
                    if value[i] != value1[j]:
                        n = n + 1
            list1.append((n, value))  
        list1 =  sorted(list1)   

        for tup in list1:
            DomainValues.append(tup[1])
        
        return DomainValues


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """

        list1 = list()

        for var in self.crossword.variables - set(assignment):
            n = len(self.domains[var])
            n2 = len(self.crossword.neighbors(var))
            list1.append((n, n2, var))
        list1 = sorted(list1, key = lambda x: x[0])
        BestTup = (0, 0, None)
        Variable = None
        for tup in list1:
            if tup[1] > BestTup[1]:
                BestTup = tup
                Variable = BestTup[2]
        
        return Variable

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
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result != None:
                    return result
            assignment.pop(var)
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
