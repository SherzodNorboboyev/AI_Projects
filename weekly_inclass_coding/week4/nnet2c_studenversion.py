import argparse
import os.path
import sys
import time

from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf

import tensorflow.contrib.slim as slim

from tensorflow.examples.tutorials.mnist import input_data
from tensorflow.examples.tutorials.mnist import mnist

# Basic model parameters as external flags.
FLAGS = None


def placeholder_inputs(batch_size):
    """Generate placeholder variables to represent the input tensors.
  These placeholders are used as inputs by the rest of the model building
  planner_v2 and will be fed from the downloaded data in the .run() loop, below.
  Args:
    batch_size: The batch size will be baked into both placeholders.
  Returns:
    images_placeholder: Images placeholder.
    labels_placeholder: Labels placeholder.
  """
    # Note that the shapes of the placeholders match the shapes of the full
    # image and label tensors, except the first dimension is now batch_size
    # rather than the full size of the train or test data sets.
    images_placeholder = tf.placeholder(tf.float32, shape=(batch_size,
                                                           mnist.IMAGE_PIXELS))
    labels_placeholder = tf.placeholder(tf.int32, shape=(batch_size))
    return images_placeholder, labels_placeholder


def fill_feed_dict(data_set, images_pl, labels_pl):
    """Fills the feed_dict for training the given step.
  A feed_dict takes the form of:
  feed_dict = {
      <placeholder>: <tensor of values to be passed for placeholder>,
      ....
  }
  Args:
    data_set: The set of images and labels, from input_data.read_data_sets()
    images_pl: The images placeholder, from placeholder_inputs().
    labels_pl: The labels placeholder, from placeholder_inputs().
  Returns:
    feed_dict: The feed dictionary mapping from placeholders to values.
  """
    # Create the feed_dict for the placeholders filled with the next
    # `batch size` examples.
    images_feed, labels_feed = data_set.next_batch(FLAGS.batch_size,
                                                   FLAGS.fake_data)
    feed_dict = {
        images_pl: images_feed,
        labels_pl: labels_feed,
    }
    return feed_dict


class somenetclass():
    def __init__(self, dim_in):
        self.dim_in = dim_in

        self.paramsdict = {}
        self.layerdict = {}

        stddev = 0.1

        # creates weights that map self.dim_in onto dimension 100
        self.paramsdict['w1'] = tf.get_variable(name='w1', shape=[self.dim_in, 250],
                                                initializer=tf.random_normal_initializer(0, (2.0 / self.dim_in) ** 0.5))
        self.paramsdict['b1'] = tf.get_variable(name='b1', shape=[1, 250], initializer=tf.constant_initializer(0))

        ################################################################
        ################################################################
        ################################################################
        # !!STUDENTS:
        ################################################################
        ################################################################
        ################################################################
        self.paramsdict['w2'] = tf.get_variable(name='w2', shape=[250, 100],
                                                initializer=tf.random_normal_initializer(0, (2.0 / self.dim_in) ** 0.5))
        self.paramsdict['b2'] = tf.get_variable(name='b2', shape=[1, 100], initializer=tf.constant_initializer(0))

        self.paramsdict['w3'] = tf.get_variable(name='w3', shape=[100, 10],
                                                initializer=tf.random_normal_initializer(0, (2.0 / self.dim_in) ** 0.5))
        self.paramsdict['b3'] = tf.get_variable(name='b3', shape=[1, 10], initializer=tf.constant_initializer(0))




    def predict(self, x):
        l1 = tf.add(tf.matmul(x, self.paramsdict['w1']), self.paramsdict['b1'])  # self.layerdict['l1']=... if you want to reuse the tensor for whatever magic



        ################################################################
        ################################################################
        ################################################################
        # !!STUDENTS:
        ################################################################
        ################################################################
        ################################################################

        l1= tf.nn.relu(l1)
        # implement two more layers: 100 neurons, and 10 neurons, both: linear, then relu
        l2 = tf.add(tf.matmul(l1, self.paramsdict['w2']), self.paramsdict['b2'])
        l2 = tf.nn.relu(l2)

        l3 = tf.add(tf.matmul(l2, self.paramsdict['w3']), self.paramsdict['b3'])

        return l3
                # return must return output tensor of a linear layer, not a relu and no softmax, reason is the loss defined in run_training
        # cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
        # labels=labels_int64, logits=preds, name='cross-entropy')
        # loss =tf.reduce_mean(cross_entropy, name='cross-entropy_mean')
        #
        # it works on 'logits' that are the outputs of the linear layer


def do_eval(sess,
            eval_correct,  # the tensor to be computed
            images_placeholder,  # placeholders
            labels_placeholder,
            data_set):
    """Runs one evaluation against the full epoch of data.
  Args:
    sess: The session in which the model has been trained.
    eval_correct: The Tensor that returns the number of correct predictions.
    images_placeholder: The images placeholder.
    labels_placeholder: The labels placeholder.
    data_set: The set of images and labels to evaluate, from
      input_data.read_data_sets().
  """
    # And run one epoch of eval.
    true_count = 0  # Counts the number of correct predictions.
    steps_per_epoch = data_set.num_examples // FLAGS.batch_size
    num_examples = steps_per_epoch * FLAGS.batch_size

    for step in xrange(steps_per_epoch):
        feed_dict = fill_feed_dict(data_set,
                                   images_placeholder,
                                   labels_placeholder)
        true_count += sess.run(eval_correct, feed_dict=feed_dict)
    precision = float(true_count) / num_examples

    print('  Num examples: %d  Num correct: %d  Precision @ 1: %0.04f' %
          (num_examples, true_count, precision))

    return precision


def run_training():
    """Train MNIST for a number of steps."""
    # Get the sets of images and labels for training, validation, and
    # test on MNIST.
    data_sets = input_data.read_data_sets(FLAGS.input_data_dir, FLAGS.fake_data)

    # Tell TensorFlow that the model will be built into the default Graph.
    with tf.Graph().as_default():
        # Generate placeholders for the images and labels.
        images_placeholder, labels_placeholder = placeholder_inputs(
            FLAGS.batch_size)

        # Build a Graph that computes predictions from the inference model.
        # preds=simplenet (images_placeholder)
        simplenet = somenetclass(784)

        ################################################################
        ################################################################
        ################################################################
        # !!STUDENTS:
        ################################################################
        ################################################################
        ################################################################
        # preds= # what of simplenet to call here?? fill it please

        # Add to the Graph the Ops for loss calculation.
        labels_int64 = tf.to_int64(labels_placeholder)
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
            labels=labels_int64, logits=preds, name='cross-entropy')
        loss = tf.reduce_mean(cross_entropy, name='cross-entropy_mean')

        # Add to the Graph the Ops that calculate and apply gradients.
        tf.summary.scalar('loss', loss)
        # Create the gradient descent optimizer with the given learning rate.
        optimizer = tf.train.GradientDescentOptimizer(FLAGS.learning_rate)

        # Create a variable to track the global step.
        global_step = tf.Variable(0, name='global_step', trainable=False)

        # Use the optimizer to apply the gradients that minimize the loss
        # (and also increment the global step counter) as a single training step.
        train_op = optimizer.minimize(loss, global_step=global_step)

        # Add the Op to compare the logits to the labels during evaluation.
        eval_correct = mnist.evaluation(preds, labels_placeholder)

        # Build the summary Tensor based on the TF collection of Summaries.
        summary = tf.summary.merge_all()

        # Add the variable initializer Op.
        init = tf.global_variables_initializer()

        # Create a saver for writing training checkpoints.
        saver = tf.train.Saver()

        # Create a session for running Ops on the Graph.
        sess = tf.Session()

        # Instantiate a SummaryWriter to output summaries and the Graph.
        summary_writer = tf.summary.FileWriter(FLAGS.log_dir, sess.graph)
        # summary_writer.flush()
        # And then after everything is built:

        # Run the Op to initialize the variables.
        sess.run(init)

        # Start the training loop.


        for step in xrange(FLAGS.max_steps):
            start_time = time.time()

            # Fill a feed dictionary with the actual set of images and labels
            # for this particular training step.
            feed_dict = fill_feed_dict(data_sets.train,
                                       images_placeholder,
                                       labels_placeholder)

            # Run one step of the model.  The return values are the activations
            # from the `train_op` (which is discarded) and the `loss` Op.  To
            # inspect the values of your Ops or variables, you may include them
            # in the list passed to sess.run() and the value tensors will be
            # returned in the tuple from the call.
            _, loss_value = sess.run([train_op, loss],
                                     feed_dict=feed_dict)

            duration = time.time() - start_time

            # Save a checkpoint and evaluate the model periodically.
            if (step + 1) % 1000 == 0 or (step + 1) == FLAGS.max_steps:
                checkpoint_file = os.path.join(FLAGS.log_dir, 'model_iter' + str(step) + '.ckpt')
                saver.save(sess, checkpoint_file, global_step=step)
                # Evaluate against the training set.
                print('Training Data Eval:')
                do_eval(sess,
                        eval_correct,
                        images_placeholder,
                        labels_placeholder,
                        data_sets.train)
                # Evaluate against the validation set.
                print('Validation Data Eval:')
                do_eval(sess,
                        eval_correct,
                        images_placeholder,
                        labels_placeholder,
                        data_sets.validation)
                # Evaluate against the test set.
                print('Test Data Eval:')
                do_eval(sess,
                        eval_correct,
                        images_placeholder,
                        labels_placeholder,
                        data_sets.test)

                # python -m tensorflow.tensorboard --logdir=/tmp/tensorflow/mnist/logs/fully_connected_feed

            # Write the summaries and print an overview fairly often.
            if step % 100 == 0:
                # Print status to stdout.
                print('Step %d: loss = %.2f (%.3f sec)' % (step, loss_value, duration))
                # Update the events file.
                summary_str = sess.run(summary, feed_dict=feed_dict)
                summary_writer.add_summary(summary_str, step)
                summary_writer.flush()


def main(_):
    if tf.gfile.Exists(FLAGS.log_dir):
        tf.gfile.DeleteRecursively(FLAGS.log_dir)
    tf.gfile.MakeDirs(FLAGS.log_dir)
    run_training()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--learning_rate',
        type=float,
        default=0.01,
        help='Initial learning rate.'
    )
    parser.add_argument(
        '--max_steps',
        type=int,
        default=9000,
        help='Number of steps to run trainer.'
    )
    parser.add_argument(
        '--batch_size',
        type=int,
        default=21,
        help='Batch size.  Must divide evenly into the dataset sizes.'
    )
    parser.add_argument(
        '--input_data_dir',
        type=str,
        default='/tmp/tensorflow/mnist/input_data',
        help='Directory to put the input data.'
    )
    parser.add_argument(
        '--log_dir',
        type=str,
        default='/tmp/tensorflow/mnist/logs/fully_connected_feed',
        help='Directory to put the log data.'
    )
    parser.add_argument(
        '--fake_data',
        default=False,
        help='If true, uses fake data for unit testing.',
        action='store_true'
    )

    FLAGS, unparsed = parser.parse_known_args()
tf.app.run(main=main, argv=[sys.argv[0]] + unparsed)
