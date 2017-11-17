import tensorflow as tf

class Model:
    def __init__(self):
        pass
    def model(self, num_input, num_class):
        hidden_units1 = 27
        hidden_units2 = 12
        print "building model"


        X = tf.placeholder(tf.float32, shape=[None, num_input], name='X')

        W1 = tf.Variable(tf.random_normal([num_input, hidden_units1]), name="W1")
        B1 = tf.Variable(tf.random_normal([hidden_units1]) , name="B1")
        A1 = tf.nn.softmax(tf.matmul(X, W1) + B1,  name="A1")

        W2 = tf.Variable(tf.random_normal([hidden_units1, hidden_units2]))
        B2 = tf.Variable(tf.random_normal([hidden_units2]))
        A2 = tf.nn.softmax(tf.matmul(A1, W2) + B2)

        W3 = tf.Variable(tf.random_normal([hidden_units2, num_class]))
        B3 = tf.Variable(tf.random_normal([num_class]))
        Y_ = tf.nn.softmax(tf.matmul(A2, W3) + B3, name="Y_")

        Y = tf.placeholder(tf.float32, shape=[None, num_class], name='Y')

        cross_entropy = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(Y_), reduction_indices=[1]))
        train_step = tf.train.GradientDescentOptimizer(0.005).minimize(cross_entropy)

        self.X, self.Y,self.Y_, self.train_step = (X, Y, Y_, train_step)
    def model_train_init(self, x_train, y_train, epochs):
        # new_graph = self.g_1
        with tf.Session() as sess:
            tf.global_variables_initializer().run()
            for i in range(epochs):
                sess.run(self.train_step, feed_dict={self.X: x_train, self.Y: y_train})
                if i%500 == 0:
                    print "{} / {} done".format(i, epochs)
            saver = tf.train.Saver()
            self.sess = sess
            saver.save(sess, 'my_test_model')
    def model_train_new(self, x_train, y_train, epochs):
        sess = self.sess
        for i in range(epochs):
            sess.run(self.train_step, feed_dict={self.X: x_train, self.Y: y_train})
            if i%500 == 0:
                print "{} / {} done".format(i, epochs)
    def predict(self, x_test):
        new_graph = tf.Graph()
        with tf.Session(graph=new_graph) as sess:
            saver = tf.train.import_meta_graph('my_test_model.meta')
            saver.restore(sess,tf.train.latest_checkpoint('./'))
            graph = tf.get_default_graph()
            X = graph.get_tensor_by_name("X:0")
            Y_ = graph.get_tensor_by_name("Y_:0")
            y_list, y  = sess.run([Y_, tf.argmax(Y_,1)], feed_dict={X:x_test})
            return (y[0], y_list.tolist())
    def test(self, x_test, y_test):

        sess = tf.Session()
        correct_prediction = tf.equal(tf.argmax(self.Y,1), tf.argmax(self.Y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        predicted_y = sess.run(accuracy, feed_dict={self.X: x_test, self.Y:y_test})
        print predicted_y
