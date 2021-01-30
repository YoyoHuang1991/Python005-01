CREATE TABLE `book` ( 
    `book_id` int(11) NOT NULL AUTO_INCREMENT, 
    `type_id` int(11) NOT NULL, 
    `book_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL, 
    PRIMARY KEY (`book_id`) USING BTREE, 
    ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ;


SELECT DISTINCT book_id, book_name, count(*) as  number  # 5
FROM book JOIN author ON book.sn_id = author.sn_id       # 1
WHERE pages > 500       # 2
GROUP BY book.book_id   # 3
HAVING number > 10      # 4
ORDER BY number         # 6
LIMIT 5                 # 7
