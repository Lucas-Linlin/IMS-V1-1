"""
A library management system.
It use a class and some function to do this.
"""
from tkinter import *
from doctest import testmod
import os
import sys

base_dir = os.path.dirname(__file__)
filePath = os.path.join(base_dir, "books.csv")

ISBN = "isbn"
NAME = "name"
IN = "in"
OUT = "out"
STATUS = {IN:"正常", OUT:"出借"}
FONTL = "仿宋 11"  # Label display font
FONTT = "等线Light 11"  # Text display font
FONTB = "仿宋 11 bold"  # Button font
BTNCFG = {"width":8,"height":4,"bd":5,"font":FONTB}
BUTTONS = ["green 添加书","orange 删除书","yellow 出借","blue 归还"]

class ISBNError(RuntimeError):pass
class BorrowError(RuntimeError):pass

class Book:
    """
    A book class.
    Each instance represents a book and 
    contains two attributes: "isbn" and 
    "name". A list of "Book" classes 
    represents some books (or a bookshelf).
    >>> myBook1 = Book(isbn=9787115612366, name="book1")
    >>> myBook1
    Book(ISBN:9787115612366, name:book1)
    >>> myBook2 = Book(isbn=1234,name="book2")
    Traceback (most recent call last):
        ...
    main.ISBNError: not a effective ISBN code.
    """
    def __init__(self, isbn, name):
        if len(str(isbn)) != 13:
            raise ISBNError("not a effective ISBN code.")
        self.isbn = isbn
        self.name = name
        self.status = IN
    
    def __repr__(self):
        """
        A string tool.
        >>> book1 = Book(isbn=9787115612366,name="book1")
        >>> book1
        Book(ISBN:9787115612366, name:book1)
        >>> repr(book1)
        'Book(ISBN:9787115612366, name:book1)'
        """
        return f"Book(ISBN:{self.isbn}, name:{self.name})"
    
    def outBook(self):
        """Borrow the book.
        >>> book1 = Book(isbn=9787115612366,name="book1")
        >>> book1.status
        'in'
        >>> book1.outBook()
        >>> book1.status
        'out'
        >>> book1.outBook()
        Traceback (most recent call last):
            ...
        main.BorrowError: book has already been lend."""
        if self.status == IN:
            self.status = OUT
        else:
            raise BorrowError("book has already been lend.")
    
    def inBook(self):
        """Return the book."""
        self.status = IN

class BookShelf:
    '''A class to indicate bookshelfs.
    It use a list to indicate books on the bookshelf.
    There are books(class Book, line 27) in the list.
    >>> myBookshelf = BookShelf("97870001"="book1","97870002"="book2")
    >>> myBookShelf
    Books:
    97870001  - - - - -  book1
    97870002  - - - - -  book2
    >>> myBookshelf2 = BookShelf("9787000a"="book3")
    Traceback(most call recently):
        ...
    main.ISBNError: not a effective ISBN code.'''
    def __init__(self,**books):
        if len(books) == 0:
            self._books = []
            self.isbns = []
        else:
            try:
                self._books = books.values()
                self.isbns = [int(i) for i in books.keys()]
            except:
                raise ISBNError("not a effective ISBN code.")
         
    def readFromFile(self):
        with open(filePath,encoding="utf-8") as fileObj:
            for line in fileObj:
                line = line.rstrip("\n")
                isbn,name = line.split(",")
                isbn=int(isbn)
                self._books.append(Book(isbn, name))
                self.isbns.append(isbn)

    def writeToFile(self):
        with open(filePath,mode="w",encoding="utf-8") as fileObj:
            for i in self._books:
                fileObj.write(f"{i.isbn},{i.name}\n")
    def addBook(self):
        createAddWin()
        global window1,B1,L1,L2
        window1.deiconify()

    def subBook(self):
        createSubWin()
        global window2,B2,L3,L4
        #window2.deiconify()

    def __iter__(self):
        return iter(self._books)
    
    def __getitem__(self,index):
        for i in self._books:
            if i.isbn == index or i.name == index:
                return i

    def findBook(self,isbn):
        """Return book which has the ISBN.
        >>> books = BookShelf()
        >>> books.append(Book(isbn=9787115612366,name="流畅的Python"))
        >>> myBook = findBook(9787115612366)
        >>> myBook
        Book(ISBN:9787115612366, name:流畅的Python)"""
        for i in self._books:
            if i.isbn == isbn:
                return i
            
    def append(self,book):
        self._books.append(book)

    def pop(self,isbn):
        self._books.pop(isbn)
    
    def __repr__(self):
        returnStr = f"Books:\n"
        for i in self:
            isbn, name = i.isbn, i.name 
            returnStr += f"{isbn}  - - - - -  {name}"
        return returnStr

def exitAskAdd():
    global books,window1
    try:
        L1.config(text="ISBN:",fg="black")
        name = E2.get()
        isbn = E1.get()
        isbn = int(isbn)
        if name == "":
            L2.config(text="名称 输入不正确",fg="red")
            E2.delete(0,END)
            return
        
        elif isbn in books.isbns:
            print(books.isbns)
            L1.config(text="ISBN 输入不正确",fg="red")
            E1.delete(0,END)
            return
        books.append(Book(isbn,name))
        books.writeToFile()
        updateScreen()
        window1.destroy()
        
    except:
        print("err no. 1")
        L1.config(text="ISBN 输入不正确",fg="red")
        E1.delete(0,END)
        return

def exitAskSub():
    global books,window2
    try:
        L3.config(text="ISBN:",fg="black")
        isbn = int(E3.get())
        for j,i in enumerate(books):
            if i.isbn == isbn:
                books.pop(j)
        books.writeToFile()
        updateScreen()
        window2.destroy()
    except:
        L3.config(text="ISBN 输入不正确",fg="red")
        E3.delete(0,END)
        return
    

def updateScreen():
    global numText,isbnText,nameText,statusText

    numText.config(state=NORMAL)
    isbnText.config(state=NORMAL)
    nameText.config(state=NORMAL)
    statusText.config(state=NORMAL)

    numText.delete(1.0,END)
    isbnText.delete(1.0,END)
    nameText.delete(1.0,END)
    statusText.delete(1.0,END)

    for j,i in enumerate(books):
        numText.insert(END,f" {j+1}\n\n")
        isbnText.insert(END,f"({j+1}) {i.isbn}\n\n")
        nameText.insert(END,f"({j+1})  {i.name}\n\n")
        statusText.insert(END,f"({j+1}) {STATUS[i.status]}\n\n")
        
    numText.config(state=DISABLED)
    isbnText.config(state=DISABLED)
    nameText.config(state=DISABLED)
    statusText.config(state=DISABLED)

def main():
    """
    The main function.
    Has all(bushi) elements.
    >>> main()
    """
    global root,books
    global numText,isbnText,nameText,statusText

    books=BookShelf()

    books.readFromFile()
    root = Tk()
    root.title("图书馆管理系统")

    infoLab1 = Label(root,text="序号",font=FONTL)
    infoLab1.grid(column=0,row=0)

    infoLab2 = Label(root,text="ISBN",font=FONTL)
    infoLab2.grid(column=1,row=0)

    infoLab3 = Label(root,text="名称",font=FONTL)
    infoLab3.grid(column=2,row=0)

    infoLab4 = Label(root,text="状态",font=FONTL)
    infoLab4.grid(column=3,row=0)

    numText = Text(root,width=5,height=20,font=FONTT,state=DISABLED)
    numText.grid(column=0,row=1,rowspan=4)

    isbnText = Text(root,width=20,height=20,font=FONTT,state=DISABLED)
    isbnText.grid(column=1,row=1,rowspan=4)

    nameText = Text(root,width=35,height=20,font=FONTT,state=DISABLED)
    nameText.grid(column=2,row=1,rowspan=4)

    statusText = Text(root,width=10,height=20,font=FONTT,state=DISABLED)
    statusText.grid(column=3,row=1,rowspan=4)

    buttons=[]
    for j,i in enumerate(BUTTONS):
        color,text = i.split()
        buttons.append(Button(root,bg=color,text=text,**BTNCFG))
    
    addBtn, subBtn, outBtn, inBtn = buttons

    addBtn.config(command=books.addBook)
    subBtn.config(command=books.subBook)
    inBtn.config(fg="white")

    addBtn.grid(column=4,row=1)
    subBtn.grid(column=4,row=2)
    outBtn.grid(column=4,row=3)
    inBtn.grid(column=4,row=4)

    updateScreen()

def createAddWin():
    """Create a window to ask a book for add.
    >>> createAddWin()
    """
    global window1,E1,E2,B1,L1,L2
    window1 = Tk()
    window1.title("ASK")

    L1 = Label(window1,text="ISBN:",font=FONTL)
    L1.grid(column=0,row=0)

    E1 = Entry(window1,width=13,font=FONTT)
    E1.grid(column=1,row=0)

    L2 = Label(window1,text="名称:",font=FONTL)
    L2.grid(column=0,row=1)

    E2 = Entry(window1,width=13,font=FONTT)
    E2.grid(column=1,row=1)

    B1 = Button(window1,text="确定",font=FONTB,width=10,height=1,command=exitAskAdd)
    B1.grid(column=0,row=2,columnspan=2)

def createSubWin():
    """Create a window to ask a book for sub.
    >>> createSubWin()
    """
    global window2,E3,E4,B2,L3,L4
    window2 = Tk()
    window2.title("ASK")

    L3 = Label(window2,text="ISBN:",font=FONTL)
    L3.grid(column=0,row=0)

    E3 = Entry(window2,width=13,font=FONTT)
    E3.grid(column=1,row=0)

    B2 = Button(window2,text="确定",font=FONTB,width=10,height=1,command=exitAskSub)
    B2.grid(column=0,row=2,columnspan=2)

if __name__ == "__main__":
    main()
    root.mainloop()