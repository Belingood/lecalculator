>
> # LECalculator
>
> Long Expression Calculator 0.1

## Engine

**There are three main working blocks in the LECalculator:**

> ### CALCULATOR

> ### TESTS

> ### API

## Calculator

### LECalculator is written in PYTHON

Although this calculator was created for the needs of the API, it can be used as a standalone module. As input, it takes a mathematical expression in the string format of the following form:

> `"15 + ((7 - 3) * 14) / 9 - 5"`

In this it is similar to the **eval** standard Python function, but unlike it, the **LECalculator** uses the **decimal** module for calculations, which provides more accurate calculation results, especially in operations with real numbers.

### Example

> **Expression:** `"0.1 + 0.1 + 0.1"`
> 
> **Eval result:** `0.30000000000000004`
> 
> **LECalculator result:** `"0.3"`

### Zero Division problem

Since this calculator is designed to work with rather long expressions, in the case when division by zero is included somewhere in the depth of this expression, the calculator does not just throw an exception, but indicates the sector in which this error occurred:

### Example

> #### Expression: `"16 + 4 - 10 / 0 + 12 * 4"`
> 
> #### LECalculator result: `"16+4-{ZeroDivisionError}+12*4"`

However, it should be noted that the expression will not be returned in its original form, but in the calculated form up to the level at which the computational process was interrupted by the exception:

### Example

> **Expression:** `"2 / (16 - (24 / 3) * 2) - 9 / (25 * 4)"`
> 
> **LECalculator result:** `"{ZeroDivisionError}-9/100"`

### Input validation and calculating

The calculator module has a function to check the input expression:

> ### data_checker
> *the function for check the input expression*

It can be used standalone for pre-validation of data, and this function also participates in the validation of incoming data inside the main function:

> ### calculator
> *the main function for calculating the result*

### Mathematical operations

Four basic operations are available on the current version: **addition**, **subtraction**, **multiplication**, **division**.

> The result is returned in string format.

### Practical use examples

> `>>> lec = LECalculator()`
> 
> `>>> exp = "7 + 4 - 1 * 2"`
> 
> `>>> lec.data_checker(exp)`
> 
> True
> 
> `>>> lec.calculator(exp)`
> 
> '9'

>`>>> exp = "8.3 * (9 - 7.2) + 3.128"`
> 
> `>>> LECalculator.data_checker(exp)`
> 
> True
> 
> `>>> LECalculator.calculator(exp)`
> 
> '18.068'

> `>>> LECalculator.calculator('5 * 2 - (6 + 5)')`
> 
> '-1'

## Tests

The presented product is equipped with a testing module that runs on **Python Unittes**.

The testing process covers practically all working methods of the program. The test results are automatically entered into a database.

> This version of the program uses a **PostgreSQL** relational database. But, if necessary, of course, you can integrate any type of data storage.

## API

The main file contains a function that implements the processing of a **GET** request from a client, of the following form:

> http://my-app/calculator/5+5+5/2*4.7

As a response, the client receives a JSON object of the following form:

> code 200
> 
> {
>
> "result": "21.75"
> 
> }

In case of an incorrect request, an error message with a status code 404 is sent as a response:

> http://my-app/calculator/5-(4+3))
>
> code 404
> 
> {
>
> "detail": "Please check the sent data. The expression must contain only .()/*-+0123456789"
> 
> }

> http://my-app/calculator/4+5/0
>
> code 404
> 
> {
>
> "detail": "ZeroDivisionError: 4+5/0 --> 4+{ZeroDivisionError}"
> 
> }

Where **my-app** is your working domain or localhost.

**The results of all requests, including incorrect ones, are entered into the database.**

> This version of the program uses a **PostgreSQL** relational database. But, if necessary, of course, you can integrate any type of data storage.
 
**Please note that the presented version contains only the server part of the program.**

## Installation information

+ All necessary packages and dependencies are in the **requirements.txt** file
+ The database (PostgreSQL) configuration data is in the **database.ini** file. **Be sure to replace the data in this file with your own.**
+ To create database tables, use the command: `>>> python create_table.py`
+ To test the installed program, you can use the **FastAPI docs** by going to http://my-app/docs

