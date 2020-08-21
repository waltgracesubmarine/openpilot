This branch is to help you live tune your pre-existing proportional-and-integral-controlled car. ***Currently only steering tuning is supported***

1. Start opEdit by running:

       python /data/openpilot/op_edit.py
2. Make sure you're in live tuning mode by typing `live` if not already, after completing opEdit setup.
3. You'll see three parameters:
    - `p_multiplier`: proportional multiplier
    - `i_multiplier`: integral multiplier
    - `d_gain`: derivative gain (the actual derivative gain)

    P and I parameters are simply multiplied by your car's pre-existing tuning values. Once you find good P and I multipliers, multiply your car's P and I gains by the multipliers and replace with the gains on your fork/branch or open a PR to this fork.

    ***Note: The `d_gain` parameter is the actual derivative tuning gain since most cars do not have derivative added at all. This value will go into your interface file on a full PID supported fork, without any pre-multiplication.***
