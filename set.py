#以学校日常水果品种为例

first_day_fruit = set(['apple','orange','strawberry','pear'])
second_day_fruit = set(['banana','apple','watermellon','cherry','strawberry'])

union_fruit = first_day_fruit.union(second_day_fruit)
intersection_fruit = first_day_fruit.intersection(second_day_fruit)
diff_fruit_first = first_day_fruit.difference(second_day_fruit)
diff_fruit_second = second_day_fruit.difference(first_day_fruit)

print('first day fruit is: {4}\n'
    'Second day fruit is: {5}\n'
    '并集: {0}\n'
    '交集: {1}\n'
    'first day 差集: {2}\n'
    'second day 差集: {3}\n'.format(union_fruit,intersection_fruit,diff_fruit_first,diff_fruit_second,first_day_fruit,second_day_fruit ))