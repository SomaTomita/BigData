# An Introduction to Decision Trees

We're now going to move onto something that traditional statistics doesn't do directly — classification. Specifically, we're going to look at a classification technique known as "decision tree learning".

Decision tree learning produces a "machine" into which you can input one or more attributes of an example and get out a classification. It is very similar to linear regression, except that:

1. The output variable is categorical rather than numeric
2. Input variables may be categorical as well as numeric

For example, given a set of observations about decisions made by a government agency that classifies films in terms of minimum audience (similar to the [BBFC](https://www.bbfc.co.uk/) in the UK), we can learn a decision tree model that will assign an age rating to a film based on its content. Imagine we start with the data below:

### Film Classification Truth Table

| Film | Swearing | Violence | Drug use | Age rating |
| ---- | -------- | -------- | -------- | ---------- |
| 1    | TRUE     | TRUE     | TRUE     | 18         |
| 2    | TRUE     | TRUE     | TRUE     | 18         |
| 3    | TRUE     | TRUE     | FALSE    | 15         |
| 4    | TRUE     | FALSE    | TRUE     | 15         |
| 5    | TRUE     | TRUE     | FALSE    | 15         |
| 6    | FALSE    | TRUE     | FALSE    | 12         |

If we feed that table into a decision tree learner, we could get a tree like this:

```
                    Root
                  [Swearing]
                  /        \
                 /          \
              True         False
               /             \
              /               \
          [Drugs]            [12]
           /    \
          /      \
       True     False
        /         \
       /           \
     [18]         [15]
```

_Figure 1: A decision tree for movies age rating._

In the decision tree above, false leads from there to a prediction of "12". True leads to "drugs", in turn leading to "18" if true and "15" if false.

If we run that for all the examples in our table, we can see that it can correctly predict the age rating in most cases:

### Table Showing Predicted Age Ratings

| Film | Swearing | Violence | Drug use | Actual age rating | Predicted age rating |
| ---- | -------- | -------- | -------- | ----------------- | -------------------- |
| 1    | TRUE     | TRUE     | TRUE     | 18                | 18                   |
| 2    | TRUE     | TRUE     | TRUE     | 18                | 18                   |
| 3    | TRUE     | TRUE     | FALSE    | 15                | 15                   |
| 4    | TRUE     | FALSE    | TRUE     | 15                | 18                   |
| 5    | TRUE     | TRUE     | FALSE    | 15                | 15                   |
| 6    | FALSE    | TRUE     | FALSE    | 12                | 12                   |

Film 4 is an exception — the tree predicts that it should receive an 18 certificate, but the film classification board has in fact given it only a 15. Depending on the context, this error might or might not be a significant problem.

## Summary

Decision trees are very useful for doing simple classification that works from categorical variables to produce categorical predictions. They can also be quite effective with numerical input variables, provided that the variable range falls meaningfully into continuous regions. The models they produced are easy to understand, particularly when the number of input variables is small.
