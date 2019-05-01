import time
from pretend import stub
"""
_schedule
args:
    function
    args
    time

    - it schedules a function to run at a specified time, using the provided argument
"""

from cosmotweet.scheduler import _schedule
def test__schedule():
    testfunc = lambda x: print(x + 1)
    arg = (1,)
    time_ = 0.01

    _schedule(testfunc, arg, time_)


"""
    - it can mutate object properties with scheduled functions asynchronously
"""
def test__schedule_can_set_class_state():
    test_object = stub(soul='A very good soul')

    def testfunc(obj):
        obj.soul = 'A naughty soul'

    arg = test_object
    time_ = 0.01

    _schedule(testfunc, arg, time_)

    assert test_object.soul == 'A very good soul'
    time.sleep(time_)
    assert test_object.soul == 'A naughty soul'


if __name__ == '__main__':
    test__schedule()
