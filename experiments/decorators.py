""" decorators around fastapi routes
call with: `uvicorn decorators:app --reload` or `python decorators.py` """

import random
from functools import wraps
from fastapi.responses import RedirectResponse

import uvicorn
from fastapi import Depends, FastAPI

app = FastAPI()

""" DECORATORS """


def log_decorator(log_enabled):
    """ decorator that takes an argument
    think of this as a closure of a decorator """

    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if log_enabled:
                print("Log enabled")
            else:
                print("Log disabled")
            return func(*args, **kwargs)

        return wrapper

    return actual_decorator


def async_decorator(func):
    """ async decorator w/o an argument
    main difference is you have to await the returned function """

    @wraps(func)
    async def wrapper(*args, **kwds):
        print("Calling decorated function")

        # half the time we redirect to goodbye just to demonstrate we can manipulate the response
        if random.randint(1, 2) % 2 == 0:
            return RedirectResponse("/goodbye")

        # we need to await the function since it's a async
        return await func(*args, **kwds)

    return wrapper


def async_decorator_with_argument(time_to_eat):
    """ async decorator w/ an arg
    We use a closure to capture the argument in the decorator
    Await the returned async function
    """

    def actual_decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            print(time_to_eat)
            return await func(*args, **kwargs)

        return wrapper

    return actual_decorator


""" DEPENDENCIES """


def greeting_dependency():
    """ Dependency: to show we can use dependencies w/ decorators """

    print("Calling dependency function")
    if random.randint(1, 2) % 2 == 0:
        yield "Hello World"
    else:
        yield "Howdy"


""" ROUTES """


@app.get("/log")
@log_decorator(False)
def log_endpoint():
    """ route that uses a decorator w/ an argument
    note that the decorator needs to be placed AFTER the fastapi route decorator
    modifying the input to log_decorator e.g.: True, changes print statements: Log enabled/disabled """
    return {"message": "logging"}


@app.get("/greet")
@async_decorator
async def greet(greeting=Depends(greeting_dependency)):
    """ async method that half the time will redirect us to goodbye
    Our greeting is also randomized by our dependency """
    return {"message": f"{greeting}"}


@app.get("/", dependencies=[Depends(greeting_dependency)])
@async_decorator
async def root():
    """ Dependency is "static". Value of Depends doesn't get passed into function
    we still get redirected half the time though """
    return {"message": "Hello World"}


@app.get("/lunch")
@async_decorator_with_argument("now")
async def lunch():
    """ Async method using decorator with argument """
    return {"message": "lunchtime"}


@app.get("/goodbye")
async def goodbye():
    """ used in our randomized redirect """
    return {"message": "Goodbye"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
