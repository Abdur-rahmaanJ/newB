# TODO
## Plan
```
[ ] Tokenizer module
 |__ [ ] Token class
 |    |__ [ ] Type info
 |    |__ [ ] Value
 |    |__ [ ] Position: index, line, position at line
 |
 |__ [ ] Rules list
 |    |__ [ ] Regex rule
 |    |__ [ ] Parsing layer(default: 'main')
 |    |__ [ ] Action on parse: ignore(like whitespaces), change layer(For strings tokenization)
 |
 |__ [ ] Tokenization
 
[ ] Parser module
 |__ [ ] AST
 |    |__ [ ] Block
 |    |__ [ ] Expression
 |    |__ [ ] Binary(2) operation
 |    |__ [ ] Unary(1) operation
 |    |__ [ ] Constant
 |    |__ [ ] Variable
 |    |__ [ ] Class
 |    |__ [ ] Function
 |    |__ [ ] Special constructions(loops, etc)
 |
 |___ [ ] Parsing
```

## Information
### Tokenization
...

## Notes
white spaces completely ignored !
