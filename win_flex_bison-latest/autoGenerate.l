%option noyywrap
%{
    int wordCnt = 0;
    int charCounter=0;
    int column =0,line=1;
    void addLine(int);
    void addColumn(int);
    void clearColumn();
    void addChar(int);
    void addWord(int);
%}
ID             ("_"|{letter})({letter}|{digit})*
int                    {digit}+
float                  {digit}*(\.{digit}+)?(e|E[+\-]?{digit}+)?
opt               "-"|"+"|"="|"=="|"*"|"/"|"<="|">="|"!"|"!="|"%"|"&&"|"||"|">"|"<"
sep             "("|")"|"{"|"}"|";"|","
blk           (\/\/.*\n)
multiblk		"/*"((\*+[^/*])|([^*]))*\**"*/"
char                   (\'.\')|(\'(("\\n")|("\\t"))\')
string                 \"[^\"]*\"
letter                 [A-Za-z_]
digit                  [0-9]
key            "main"|"char"|"int"|"float"|"break"|"const"|"return"|"void"|"continue"|"do"|"while"|"if"|"else"|"for"


error_char                \'[^']{4}
error_str              \"[(^")|(^\n)]*
error_ID          ({digit}|{digit}*(\.{digit}+)?(e|E[+\-]?{digit}+)?)({letter}|{digit})*{letter}({letter}|{digit})*
error_blk         "/*"[^"*/"]*
INT_HEX_ERROR 0[xX][a-fA-F0-9]*[g-zG-Z]+[a-fA-F0-9]*
INT_OCT_ERROR 0[0-7]*[89]+[0-7]*
INT_BIN_ERROR 0[bB][01]*[2-9]+[01]*
%%

{blk}  {
    addChar(yyleng);
    clearColumn();
    addLine(1);
}
{multiblk}  {
    addChar(yyleng);
    clearColumn();
    addLine(1);
}
{char}  {
    printf("Line=%3d,Column=%3d :@CHAR@%s\n",line,column,yytext);
    addChar(yyleng);
    addColumn(yyleng);
}
{string}    {
    printf("Line=%3d,Column=%3d :@STR@%s\n",line,column,yytext);
    addColumn(yyleng);
    addChar(yyleng);
}
{key} {
    printf("Line=%3d,Column=%3d :@关键字@%s\n",line,column,yytext);
    addChar(yyleng);
    addColumn(yyleng);
    addWord(1);
}
{ID}    {
    printf("Line=%3d,Column=%3d :@ID@%s\n",line,column,yytext);
    addChar(yyleng);
    addColumn(yyleng);
    addWord(1);
}

{int}   {
    addChar(yyleng);
    addColumn(yyleng);
    printf("Line=%3d,Column=%3d :@INT@%s\n",line,column,yytext);
}
{float} {
    addChar(yyleng);
    addColumn(yyleng);
    printf("Line=%3d,Column=%3d :@FLOAT@%s\n",line,column,yytext);
}
{opt}  {
    addColumn(1);
    addChar(1);
    printf("Line=%3d,Column=%3d :@操作符@%s\n",line,column,yytext);
}

{sep} {
    addColumn(1);
    addChar(1);
    printf("Line=%3d,Column=%3d :@界符@%s\n",line,column,yytext);
}
{INT_HEX_ERROR}|{INT_BIN_ERROR}|{INT_OCT_ERROR} {
    addChar(yyleng);
    addColumn(yyleng);
    printf("错误(Line=%3d,Column=%3d): 错误的int: %s\n",line,column,yytext);
}
{error_str} {
    addChar(yyleng);
    addColumn(yyleng);
    printf("错误(Line=%3d,Column=%3d): 错误的string: %s\n",line,column,yytext);
}
{error_ID} {
    addChar(yyleng);
    addColumn(yyleng);
    printf("错误(Line=%3d,Column=%3d): 错误的标识符: %s\n",line,column,yytext);
}
{error_char}   {
    addChar(yyleng);
    addColumn(yyleng);
    printf("错误(Line=%3d,Column=%3d): 错误的char: %s\n",line,column,yytext);
}
{error_blk}   {
    addChar(yyleng);
    addColumn(yyleng);
    printf("错误(Line=%3d,Column=%3d): 错误的注释: %s\n",line,column,yytext);
}
.       {
    addChar(1);
    addColumn(1);
}

\n      {
    addChar(1);
    addLine(1);
    clearColumn();
}

%%
int main(int argc, char **argv)
{
  if(argc > 1) {
    if(!(yyin = fopen(argv[1], "r"))) {
      perror(argv[1]);
      return (1);
    }
    yylex();
  }
  return 0;
}


void addLine(int cnt)   {
    line += cnt;
}
void addColumn(int cnt) {
    column += cnt;
}
void clearColumn()  {
    column = 0;
}
void addChar(int leng)  {
    charCounter += leng;
}
void addWord(int cnt)   {
    wordCnt += cnt;
}
