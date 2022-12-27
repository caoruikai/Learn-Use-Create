# Hive `DISTINCT` removes duplicating rows (same values for all columns selected):
```
hive> SELECT col1, col2 FROM t1
    1 3
    1 3
    1 4
    2 5
hive> SELECT DISTINCT col1, col2 FROM t1
    1 3
    1 4
    2 5
hive> SELECT DISTINCT col1 FROM t1
    1
    2
```


# RANK vs DENSE_RANK

The Rank Hive analytic function is used to get rank of the rows in column or within group. Rows with equal values receive the same rank with next rank value skipped.

DENSE_RANK – It is similar to RANK, but leaves no gaps in the ranking sequence when there are ties. For example, if we rank a match using DENSE_RANK and had two players tie for second place, we would see that the two players were in second place and that the next person is ranked as third. However, the RANK function would also rank two people in second place, but the next person would be in fourth place.


# Cannot filter the data based on newly created columns

Example:

This raises an error:

```sql
select col1, count(col2) as col2_cnt
from mydb.mytable
where col2_cnt > 1
```

This is fine:

```sql
select col1, col2_cnt
from
(
    select col1, count(col2) as col2_cnt
    from mydb.mytable
)
where col2_cnt > 1

