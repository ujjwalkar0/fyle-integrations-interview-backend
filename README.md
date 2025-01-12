# Fyle Integrations Backend Challenge

## Who is this for?

This challenge is meant for candidates who wish to work / intern at Fyle and work with our engineering teams.

If it is for internship, you should be able to commit to at least 6 months.

## Why work at Fyle?

Fyle is a fast-growing Expense Management SaaS product. We are ~40 strong engineering team at the moment. 

We are an extremely transparent organization. Check out our [careers page](https://careers.fylehq.com) that will give you a glimpse of what it is like to work at Fyle. Also, check out our Glassdoor reviews [here](https://www.glassdoor.co.in/Reviews/Fyle-Reviews-E1723235.htm). You can read stories from our teammates [here](https://stories.fylehq.com).


## Challenge outline

This is a web application designed in a context of a single classroom. 
Described [here](./Application.md)

### Your tasks 
1. Add missing APIs mentioned [here](./Application.md#Missing-APIs)
2. Get the automated tests to pass
3. Get the test coverage to 90% or above
4. Feel free to add more test cases, try to increase the coverage as much as you can

## Submission

Once you are done with your task, please use [this form](https://forms.gle/Hcs7VX4YiopWwQa4A) to complete your submission.

## What happens next?

You will hear back within 48 hours from us via email. We may request for some changes based on reviewing your code.

Subsequently, we will schedule a phone interview with a Fyle Engineer.

If that goes well, we'll make an offer. 

---

## Installation
1. Fork this repository to your github account
2. Clone the forked repository and proceed with steps mentioned below

### Install requirements
```
virtualenv env --python=python3.8
source env/bin/activate
pip install -r requirements.txt
```
### Reset DB
```
rm db.sqlite3
```
### Reset Test DB
```
rm test_db.sqlite3
```
### Start Server
```
bash run.sh
```
### Run Tests
```
pytest tests/ --cov
```

## My Work
1. Write all missing APIs.
2. Add additional tests
    
    A. Test for the student, not registered with the database
    
    B. Test when no headers are provided

    C. Check if homepage loaded successfully

    D. Test for a assignment that is not exist

    E. Student try to submit assignment without teacher id

    F. Student try to set grade of assignment

    G. Test student try to set his assignment graded

## Test Report: [Details](./report.txt)

<center>

![image](https://user-images.githubusercontent.com/55041104/197340635-c816f3f6-8da7-4e82-bc8d-b1e8edf3de05.png)

</center>
