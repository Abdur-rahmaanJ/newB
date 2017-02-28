# TODO
## Plan
```
[ ] Tokenizer module
 |__ [ ] Token class
 |    |___ (X) Type info
 |    |___ (X) Value
 |    |___ ( ) Position: index, line, position at line
 |
 |__ ~~~ Rules list # Will not be added
 |    |___ ( ) Regex rule
 |    |___ ( ) Parsing layer(default: 'main')
 |    |___ ( ) Action on parse: ignore(like whitespaces), change layer(For strings tokenization)
 |
 |__ [X] Tokenization
 
[ ] Parser module
 |__ [ ] AST
 |    |___ ( ) Block
 |    |___ ( ) Expression
 |    |___ ( ) Binary(2) operation
 |    |___ ( ) Unary(1) operation
 |    |___ ( ) Constant
 |    |___ ( ) Variable
 |    |___ ( ) Class
 |    |___ ( ) Function
 |    |___ ( ) Special constructions(loops, etc)
 |
 |___ [ ] Parsing
```

## Information
### Tokenization
...

## Notes
white spaces completely ignored !
