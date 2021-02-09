01pandas簡介
====
说明：19 分 41 秒左右的 df[1:3] 应该是 df[0:3] ，这里的原理和 Python 数组的切片是一样的。

获取课程源码操作方法：
* 切换分支：git checkout 4a
* pandas 中文文档：https://www.pypandas.cn/
sklearn-pandas
* 安装参考文档：
https://pypi.org/project/sklearn-pandas/1.5.0/
* Numpy 学习文档：
https://numpy.org/doc/
* matplotlib 学习文档：
https://matplotlib.org/contents.html



04pandas數據預處理
====
Series 学习文档：
https://pandas.pydata.org/pandas-docs/stable/reference/series.html

05pandas數據調整
====
DataFrame 学习文档：
https://pandas.pydata.org/pandas-docs/stable/reference/frame.html

06pandas基本操作
====
Pandas 计算功能操作文档：
https://pandas.pydata.org/docs/user_guide/computation.html#method-summary

08pandas多表拼接
====
MySQL 数据库多表连接学习文档：
https://dev.mysql.com/doc/refman/8.0/en/join.html

09pandas輸出和繪圖
====
* plot 学习文档：
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.plot.html
* seaborn 学习文档：
http://seaborn.pydata.org/tutorial.html


10jieba分詞與提取關鍵詞
====
* jieba 学习文档：
https://github.com/fxsjy/jieba/blob/master/README.md

11SnowNLP情感傾向分析
====
* 切换分支：git checkout 4c
* jieba 学习文档：
https://github.com/fxsjy/jieba/blob/master/README.md


Homework
====
* 作业背景：
  在数据处理的步骤中，可以使用 SQL 语句或者 pandas 加 Python 库、函数等方式进行数据的清洗和处理工作。
  
  因此需要你能够掌握基本的 SQL 语句和 pandas 等价的语句，利用 Python 的函数高效地做聚合等操作。

* 作业要求：请将以下的 SQL 语句翻译成 pandas 语句：

```sql
1. SELECT * FROM data;

2. SELECT * FROM data LIMIT 10;

3. SELECT id FROM data;  //id 是 data 表的特定一列

4. SELECT COUNT(id) FROM data;

5. SELECT * FROM data WHERE id<1000 AND age>30;

6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;

7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;

8. SELECT * FROM table1 UNION SELECT * FROM table2;

9. DELETE FROM table1 WHERE id=10;

10. ALTER TABLE table1 DROP COLUMN column_name;
```