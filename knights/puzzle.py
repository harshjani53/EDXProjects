from logic import *

aKnight = Symbol("A is a Knight")
aKnaive = Symbol("A is a Knaive")

bKnight = Symbol("B is a Knight")
bKnaive = Symbol("B is a Knaive")

cKnight = Symbol("C is a Knight")
cKnaive = Symbol("C is a Knaive")


knowledge0 = And(
    Not(And(aKnight, aKnaive)), 
    Or(aKnight, aKnaive),        
    Implication(aKnight, And(aKnight, aKnaive)),
    Implication(aKnaive, Not(And(aKnight, aKnaive)))
)


knowledge1 = And(
    Not(And(aKnight, aKnaive)), 
    Or(aKnight, aKnaive),       

    Not(And(bKnight, bKnaive)),  
    Or(bKnight, bKnaive),       



    Implication(aKnight, And(aKnaive, bKnaive)),
    Implication(aKnaive, Not(And(aKnaive, bKnaive)))
)

knowledge2 = And(
    Not(And(aKnight, aKnaive)),
    Or(aKnight, aKnaive),

    Not(And(bKnight, bKnaive)),
    Or(bKnight, bKnaive),



    Implication(aKnight, And(aKnight, bKnight)),
    Implication(aKnaive, Not(And(aKnaive, bKnaive))),

    Implication(bKnight, And(bKnight, aKnaive)),
    Implication(bKnaive, Not(And(bKnaive, aKnight)))
)


knowledge3 = And(
    Not(And(aKnight, aKnaive)),
    Or(aKnight, aKnaive),

    Not(And(bKnight, bKnaive)),
    Or(bKnight, bKnaive),

    Not(And(cKnight, cKnaive)),
    Or(cKnight, cKnaive),


    Or(

        And(
            Implication(aKnight, aKnight),
            Implication(aKnaive, Not(aKnight))
        ),
        

        And(
            Implication(aKnight, aKnaive),
            Implication(aKnaive, Not(aKnaive))
        )
    ),

    Not(And(

        And(
            Implication(aKnight, aKnight),
            Implication(aKnaive, Not(aKnight))
        ),
        

        And(
            Implication(aKnight, aKnaive),
            Implication(aKnaive, Not(aKnaive))
        )
    )),


    Implication(bKnight, And(
        Implication(aKnight, aKnaive),
        Implication(aKnaive, Not(aKnaive))
    )),

    Implication(bKnaive, Not(And(
        Implication(aKnight, aKnaive),
        Implication(aKnaive, Not(aKnaive))
    ))),



    Implication(bKnight, cKnaive),
    Implication(bKnaive, Not(cKnaive)),


    Implication(cKnight, aKnight),
    Implication(cKnaive, Not(aKnight))
)


def main():
    symbols = [aKnight, aKnaive, bKnight, bKnaive, cKnight, cKnaive]
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
