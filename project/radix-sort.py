from unittest import TestCase
import urllib
import requests

def book_to_words(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii','replace')
    return bookascii.split()

def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    arr = book_to_words(book_url)
    longest = len(max(arr, key=len))
    
    for x in range(longest):
        arr = sort(arr, x, longest - 1)
    
    return arr

def sort(book, idx, max):
    out = [0 for x in range(len(book))]
    count = [0 for x in range(128)]

    for word in book:
        if max - idx < len(word):
            count[word[max - idx]] += 1
        else:
            count[0] += 1
    
    for x in range(128):
        count[x] += count[x-1]

    for x in range(len(book) -1, -1, -1):
        if max - idx < len(book[x]):
            out[count[book[x][max - idx]] - 1] = book[x]
            count[book[x][max - idx]] -= 1
        else:
            out[count[0] - 1] = book[x]
            count[0] -= 1
    
    return out