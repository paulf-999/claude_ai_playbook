Start a structured debugging session using the debugger sub-agent approach.

Ask the user to describe the problem: what was expected, what actually happened, and any error messages or logs available.

Then work through the following in order:
1. Confirm the error is reproducible and establish the environment (branch, dependencies, config)
2. Check recent changes that may have introduced the issue (`git log --oneline -10`)
3. State a working hypothesis for the root cause
4. Propose one diagnostic step to test the hypothesis — wait for the result before proceeding
5. Revise the hypothesis based on findings and repeat until root cause is confirmed
6. Propose the minimal fix once root cause is known

Do not suggest broad rewrites to fix a narrow bug. If the issue reveals a wider structural problem, flag it separately rather than addressing it inline.
