import pyparsing

File = pyparsing.Forward()

Statement = pyparsing.Forward()("STATEMENT")
FuncDef = pyparsing.Forward()("FUNCTION")
TypeBound = pyparsing.Forward()("TYPEBOUND")
Statement_With_End = pyparsing.Forward()("SWE")
Statement_Without_End = pyparsing.Forward()("SWOE")
BlockStatement = pyparsing.Forward()("BLOCK")
ReturnStatement = pyparsing.Forward()("RETURN")
AnyValue = pyparsing.Forward()("AnyValue")
IfStatement = pyparsing.Forward()("IF")
WhileStatement = pyparsing.Forward()("While")


BinExpr = pyparsing.Forward()
BoolExpr = pyparsing.Forward()
Term = pyparsing.Forward()
Factor = pyparsing.Forward()
FnCall = pyparsing.Forward()("CALL")
VarDef = pyparsing.Forward()("VAR")
VarSet = pyparsing.Forward()("VAR")

BinExpr.ignore(pyparsing.python_style_comment)
BoolExpr.ignore(pyparsing.python_style_comment)
Term.ignore(pyparsing.python_style_comment)
Factor.ignore(pyparsing.python_style_comment)
VarDef.ignore(pyparsing.python_style_comment)
FnCall.ignore(pyparsing.python_style_comment)
VarSet.ignore(pyparsing.python_style_comment)
ReturnStatement.ignore(pyparsing.python_style_comment)
Statement.ignore(pyparsing.python_style_comment)

Number = pyparsing.pyparsing_common.integer()("NUMBER")
Float = pyparsing.pyparsing_common.real()("REAL")
Identifier = pyparsing.pyparsing_common.identifier()("IDENTIFIER")

String = pyparsing.Forward()
String << '"' + pyparsing.Opt(pyparsing.CharsNotIn('"'), "") + '"'

Plus = pyparsing.Literal("+")
Sub = pyparsing.Literal("-")
Mul = pyparsing.Literal("*")
Div = pyparsing.Literal("/")
Set = pyparsing.Literal("=")

Bool_Op = pyparsing.one_of(["==", "!=", "<=", ">=", ">", "<"])

Types = pyparsing.one_of(["int", "string", "float", "bool", "void"])

Keyword_Var = pyparsing.Keyword("var")
Keyword_Fn = pyparsing.Keyword("func")
Keyword_False = pyparsing.Keyword("false")
Keyword_True = pyparsing.Keyword("true")
Keyword_Return = pyparsing.Keyword("return")
Keyword_If = pyparsing.Keyword("if")
Keyword_Elif = pyparsing.Keyword("elif")
Keyword_Else = pyparsing.Keyword("else")
Keyword_While = pyparsing.Keyword("while")
Keyword_Break = pyparsing.Keyword("break")
Keyword_Continue = pyparsing.Keyword("continue")


LParen = pyparsing.Suppress("(")
RParen = pyparsing.Suppress(")")

LCurly = pyparsing.Suppress("{")
RCurly = pyparsing.Suppress("}")

End = pyparsing.Suppress(";")

BoolExpr << pyparsing.Group(BinExpr + pyparsing.ZeroOrMore(Bool_Op + BinExpr))
BinExpr << pyparsing.Group(Term + pyparsing.ZeroOrMore((Plus | Sub) + Term))
Term << pyparsing.Group(
    pyparsing.Group(Factor)
    + pyparsing.ZeroOrMore((Mul | Div) + pyparsing.Group(Factor))
)

BlockStatement << pyparsing.Group(LCurly + pyparsing.ZeroOrMore(Statement) + RCurly)
BlockStatement.ignore(pyparsing.python_style_comment)

FnCall << (
    Identifier
    + LParen
    + pyparsing.Group(pyparsing.DelimitedList(pyparsing.ZeroOrMore(BoolExpr)))
    + RParen
)

AnyValue << pyparsing.MatchFirst(
    [Float, String, Number, Keyword_False, Keyword_True, Identifier]
)

Factor << pyparsing.MatchFirst(
    [
        FnCall,
        AnyValue,
        pyparsing.Group(LParen + BoolExpr + RParen),
    ]
)

IfStatement << Keyword_If + LParen + pyparsing.ZeroOrMore(
    BoolExpr
) + RParen + BlockStatement + pyparsing.ZeroOrMore(
    Keyword_Elif + LParen + BoolExpr + RParen + BlockStatement
) + pyparsing.ZeroOrMore(
    Keyword_Else + BlockStatement
)


TypeBound << Types + Identifier

(
    VarDef
    << pyparsing.MatchFirst(
        [
            Keyword_Var + TypeBound + Set + (BoolExpr),
            Keyword_Var + TypeBound,
        ]
    )
)


(
    FuncDef
    << Keyword_Fn
    + pyparsing.DelimitedList(TypeBound, ",")
    + LParen
    + pyparsing.Group(pyparsing.DelimitedList(pyparsing.ZeroOrMore(TypeBound)))
    + RParen
    + BlockStatement
)

VarSet << Identifier + Set + BoolExpr
ReturnStatement << Keyword_Return + (BoolExpr)

WhileStatement << Keyword_While + LParen + BoolExpr + RParen + BlockStatement

Statement << pyparsing.Group(
    pyparsing.MatchFirst(
        [
            ReturnStatement + End,
            WhileStatement,
            (VarSet + End),
            VarDef + End,
            IfStatement,
            FuncDef,
            Keyword_Break + End,
            Keyword_Continue + End,
            (BoolExpr + End),
        ]
    )
)
# Statement << Statement_With_End


File.ignore(pyparsing.python_style_comment)
File << (pyparsing.ZeroOrMore((Statement)))
