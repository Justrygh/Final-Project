import tensorflow as tf
from sklearn.model_selection import train_test_split

features = None
categories = 2

x = tf.placeholder(tf.float32, [None, features])
y = tf.placeholder(tf.float32, [None, categories])
W1 = tf.Variable(tf.zeros([features, categories]))
b1 = tf.Variable(tf.zeros([categories]))

y_ = tf.sigmoid(tf.matmul(x, W1) + b1)

loss = tf.reduce_sum(tf.square(y - y_))
update = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

