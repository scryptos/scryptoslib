var dict = {
  '.-': 'A',
  '-...': 'B',
  '-.-.': 'C',
  '-..': 'D',
  '.': 'E',
  '..-.': 'F',
  '--.': 'G',
  '....': 'H',
  '..': 'I',
  '.---': 'J',
  '-.-': 'K',
  '.-..': 'L',
  '--': 'M',
  '-.': 'N',
  '---': 'O',
  '.--.': 'P',
  '--.-': 'Q',
  '.-.': 'R',
  '...': 'S',
  '-': 'T',
  '..-': 'U',
  '...-': 'V',
  '.--': 'W',
  '-..-': 'X',
  '-.--': 'Y',
  '--..': 'Z',
  '.----': '1',
  '..---': '2',
  '...--': '3',
  '....-': '4',
  '.....': '5',
  '-....': '6',
  '--...': '7',
  '---..': '8',
  '----.': '9',
  '-----': '0'
};

var fs = require('fs');
var words = fs.readFileSync('/usr/share/dict/words').toString().split('\n');
var trie = { complete: false };

for(var n = 0;n < words.length;n++) {
  var word = words[n].toUpperCase();
  if(word.replace(/[A-Z0-9]/g, '').length > 0) {
    console.log(word);
    continue;
  }
  if(word.length < 2 && word != 'I' && word != 'A')
    continue;
  var cur = trie;
  for(var i_char = 0;i_char < word.length;i_char++) {
    if(!cur[word[i_char]]) cur[word[i_char]] = { complete: false };
    cur = cur[word[i_char]];
  }
  cur.complete = true;
}

var isWord = function(str) {
  var cur = trie;
  for(var i = 0;i < str.length;i++) {
    if(!cur[str[i]]) return false;
    cur = cur[str[i]];
  }
  return cur.complete;
};
var isPrefix = function(str) {
  var cur = trie;
  for(var i = 0;i < str.length;i++) {
    if(!cur[str[i]]) return false;
    cur = cur[str[i]];
  }
  return true;
};

var isWordList = function(wordList) {
  if(wordList.length == 0) return true;
  for(var i = 0;i < wordList.length - 1;i++) {
    if(!isWord(wordList[i]))
      return false;
  }
  if(!isPrefix(wordList[wordList.length - 1]))
    return false;
  return true;
};

var isCompleteWordList = function(wordList) {
  for(var i = 0;i < wordList.length;i++) {
    if(!isWord(wordList[i]))
      return false;
  }
  return true;
};

var appendToWordList = function(wordList, c) {
  var tmp;
  var newWordLists = [];
  if(wordList.length > 0) {
    tmp = wordList.slice(0);
    tmp[tmp.length - 1] = tmp[tmp.length - 1] + c;
    newWordLists.push(tmp);
  }
  tmp = wordList.slice(0);
  tmp.push(c);
  newWordLists.push(tmp);
  return newWordLists;
};

var decodeWords = function(code) {
  var cache = {
    '0': [[]]
  };
  for(var start = 0;start < code.length;start++) {
    for(var len = 1;len < 6;len++) {
      if(start + len > code.length) continue;
      if(!cache[start + len]) cache[start + len] = [];
      var curCode = code.slice(start, start + len);
      if(dict[curCode]) {
        for(var i_start = 0;i_start < cache[start].length;i_start++) {
          wordList = cache[start][i_start];
          newWordLists = appendToWordList(wordList, dict[curCode]);
          for(var i_newWordLists = 0;i_newWordLists < newWordLists.length;i_newWordLists++) {
            if(isWordList(newWordLists[i_newWordLists]))
              cache[start + len].push(newWordLists[i_newWordLists]);
          }
        }
      }
    }
  }
  var fin = [];
  var possibleWords = cache[code.length];
  for(var i_possibleWords = 0;i_possibleWords < possibleWords.length;i_possibleWords++) {
    if(isCompleteWordList(possibleWords[i_possibleWords]))
      fin.push(possibleWords[i_possibleWords]);
  }
  fin.sort(function(a, b){return a.length - b.length;});
  return fin.map(function(a) {return a.join(' ')});
};

module.exports = decodeWords;
