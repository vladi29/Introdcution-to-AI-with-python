from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    
    #A can be Knigth or Knave, but not both:
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    #A is Kanve if only if A is not knight, in other words, A is not both
    Biconditional(AKnave, Not(And(AKnight, AKnave)))

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    #A is a knight if only if is not a knave
    Biconditional(AKnight, Not(AKnave)),
    #B is a knight if only if is not a knave
    Biconditional(BKnight, Not(BKnave)),
    #A is a knight if only if A and B are knaves both
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    
    #A is a knight if only if is not a knave
    Biconditional(AKnight, Not(AKnave)),
    #B is a knight if only if is not a knave
    Biconditional(BKnight, Not(BKnave)),
    #A is a knight if only if A and B are both knights or are both knaves
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    #B is a knight if only if A and B are different kinds
    Biconditional(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    
    #A is a knight if only if is not a knave
    Biconditional(AKnight, Not(AKnave)),
    #B is a knight if only if is not a knave
    Biconditional(BKnight, Not(BKnave)),
    #C is a knight if only if is not a knave
    Biconditional(CKnight, Not(CKnave)),
    #C is a knight if only if "A is a knight" and B is a Knave
    Biconditional(CKnight, And(AKnight, BKnave)),
    #If A is a Knight or A is a Knave then B is a Knave
    Implication(Or(AKnight, AKnave), BKnave), 
    #B is a knight if only if C is a Knave and A is a Knave 
    Biconditional(BKnight, And(CKnave, AKnave))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
