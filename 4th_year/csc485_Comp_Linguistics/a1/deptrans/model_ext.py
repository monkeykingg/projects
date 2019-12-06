#!/usr/bin/env python3
"""Statistical modelling/parsing classes"""

from itertools import islice
from pathlib import Path
from sys import stdout

import torch
import torch.nn as nn
import torch.nn.functional as F

from tqdm import tqdm

from data import load_and_preprocess_data
from data import score_arcs
from initialization import he_initializer
from parser import minibatch_parse
from util import one_hot_float


class Config(object):
    """Holds model hyperparams and data information.

    The config class is used to store various hyperparameters and dataset
    information parameters. Model objects are passed a Config() object at
    instantiation.
    """
    n_word_ids = None  # inferred
    n_tag_ids = None  # inferred
    n_deprel_ids = None  # inferred
    n_word_features = None  # inferred
    n_tag_features = None  # inferred
    n_deprel_features = None  # inferred
    n_classes = None  # inferred
    dropout = 0.5
    embed_size = None  # inferred
    hidden_size = 200
    batch_size = 2048
    n_epochs = 10
    lr = 0.001


class ParserModel(nn.Module):
    """
    Implements a feedforward neural network with an embedding layer and single
    hidden layer. This network will predict which transition should be applied
    to a given partial parse configuration.
    """
    def create_embeddings(self, word_embeddings):
        """Create embeddings that map word, tag, and deprels to vectors

        Embedding layers convert sparse ID representations to dense vector
        representations.

         - Create 3 embedding (2D) tensors, one for each of the input types.
           Input values index the rows of the matrices to extract. The
           (exclusive) max bound on the values in the input can be found in
           {n_word_ids, n_tag_ids, n_deprel_ids}.
         - The word embedding tensors should be initialized with the value of
           the argument word_embeddings; the other two matrices should be
           initialized using the He initializer you implemented.
         - Assign the tensors to self as attributes:
            self.word_embeddings
            self.tag_embeddings
            self.deprel_embeddings
           (Don't change the variable names!)
         - Make sure that gradient recording is enabled for all three embedding
           matrices (see the PyTorch tutorials for more details).

        Args:
            word_embeddings:
                numpy.ndarray of shape (n_word_ids, embed_size) representing
                matrix of pre-trained word embeddings
        """
        # *** BEGIN YOUR CODE ***
        self.word_embeddings = torch.tensor(word_embeddings, requires_grad=True)
        self.tag_embeddings = he_initializer((self.config.n_tag_ids, self.config.embed_size))
        self.tag_embeddings.requires_grad = True
        self.deprel_embeddings = he_initializer((self.config.n_deprel_ids, self.config.embed_size))
        self.deprel_embeddings.requires_grad = True
        # *** END YOUR CODE ***

    def create_weights_biases(self):
        """Create layer weights and biases for this neural network

        In our single-hidden-layer neural network, our predictions are computed
        as follows from the concatenated embedded input x:
            h = Relu(x W_h + b_h)
            h_drop = Dropout(h, dropout_rate)
            pred = h_drop W_o + b_o
        This method creates the weights and biases W_h, b_h, W_o, and b_o.

        Note that we are not applying a softmax to pred. The softmax will
        instead be done in the get_loss function, which improves efficiency
        because we can use torch.nn.functional.cross_entropy.
        Excluding the softmax in predictions won't change the expected
        transition.

         - Create the tensors mentioned above with the following dimensions:
            W_h: (N * embed_size, hidden_size)
            b_h: (hidden_size,)
            W_o: (hidden_size, n_classes)
            b_o: (n_classes,)
           where N = n_word_features + n_tag_features + n_deprel_features
         - Weight matrices should be initialized with the He initializer you
           implemented; bias vectors should be initialized to zeros.
         - Assign the weights and biases to self as attributes:
            self.W_h
            self.b_h
            self.W_o
            self.b_o
           (Don't change the variable names!)
         - Make sure that gradient recording is enabled for all of the weight
           and bias tensors (see the PyTorch tutorials for more details).
        """
        # *** BEGIN YOUR CODE ***
        N = self.config.n_word_features + self.config.n_tag_features + self.config.n_deprel_features
        self.W_h = he_initializer((N * self.config.embed_size, self.config.hidden_size))
        self.W_h.requires_grad = True
        self.b_h = torch.zeros(self.config.hidden_size, )
        self.b_h.requires_grad = True
        self.W_o = he_initializer((self.config.hidden_size, self.config.n_classes))
        self.W_o.requires_grad = True
        self.b_o = torch.zeros(self.config.n_classes, )
        self.b_o.requires_grad = True
        # *** END YOUR CODE ***

    def embedding_lookup(self, id_batch, n_ids, embedding_matrix):
        """Associate a batch of IDs (word, tag, etc.) with their embeddings

        Embedding layers convert sparse ID representations to dense vector
        representations. Inputs are integers, outputs are floats.

        Args:
            id_batch:
                torch.tensor of dtype int64 and shape (B, N) where B is the
                batch_size and N is one of {n_word_features, n_tag_features,
                n_deprel_features}.
            n_ids:
                int indicating (exclusive) maximum ID, i.e., one of
                {n_word_ids, n_tag_ids, n_deprel_ids}.
            embedding_matrix:
                torch.tensor of dtype float and shape (n_ids, embed_size).
        Returns:
            embedded_batch:
                torch.tensor of dtype float and shape (B, N * embed_size).

         - Look up the IDs specified by id_batch in embedding_matrix. This can
           be implemented as a matrix multiplication if id_batch is converted
           to one-hot vectors first. You can use the imported one_hot_float
           function from util.py for this. The shape of the one-hot tensor will
           be (B, N, n_ids), which you can then multiply with the embedding
           matrix which has shape (n_ids, embed_size) to get the relevant
           embeddings. Think about why this works.
         - The lookup results in a tensor of shape (B, N, embed_size). Reshape
           this embedded tensor into shape (B, N * embed_size). Use
           torch.reshape for this. You may find the value of -1 to be useful
           for one of the shape dimensions; see the docs for torch.reshape for
           more hints.
        """
        # *** BEGIN YOUR CODE ***
        one_hot = one_hot_float(id_batch, n_ids)
        B = id_batch.size()[0]
        N = id_batch.size()[1]
        embedded_batch = torch.mm(one_hot.view(-1, n_ids), embedding_matrix).view(B, N, -1)
        embedded_batch = torch.reshape(embedded_batch, (B, -1))
        # *** END YOUR CODE ***
        return embedded_batch

    def get_concat_embeddings(self, word_id_batch, tag_id_batch,
                              deprel_id_batch):
        """Get and concatenate word, tag, and deprel embeddings

        Recall that in our neural network, we concatenate the word, tag, and
        deprel embeddings to use as input for our hidden layer. This method
        retrieves the word, tag, and deprel embeddings and concatenates them
        together.

        Args:
            word_id_batch:
                torch.tensor of dtype int64 and shape (B, n_word_features)
            tag_id_batch:
                torch.tensor of dtype int64 and shape (B, n_tag_features)
            deprel_id_batch:
                torch.tensor of dtype int64 and shape (B, n_deprel_features)
        Returns:
            x:
                torch.tensor of dtype float and shape (B, N * embed_size) where
                N = n_word_features + n_tag_features + n_deprel_features

         - Use the self.embedding_lookup method you implemented on each of
           word_id_batch, tag_id_batch, and deprel_id_batch.
         - Concatenate the embedded inputs from the previous step together
           using torch.cat and return the result.
        """
        # *** BEGIN YOUR CODE ***
        word_embed = self.embedding_lookup(word_id_batch, self.config.n_word_ids, self.word_embeddings) 
        tag_embed = self.embedding_lookup(tag_id_batch, self.config.n_tag_ids, self.tag_embeddings)
        deprel_embed = self.embedding_lookup(deprel_id_batch, self.config.n_deprel_ids, self.deprel_embeddings)
        x = torch.cat((word_embed, tag_embed, deprel_embed), 1) 
        # *** END YOUR CODE ***
        return x

    def forward(self, word_id_batch, tag_id_batch, deprel_id_batch):
        """Compute the forward pass of the single-layer neural network

        In our single-hidden-layer neural network, our predictions are computed
        as follows from the concatenated embedded input x:
            h = Relu(x W_h + b_h)
            h_drop = Dropout(h, dropout_rate)
            pred = h_drop W_o + b_o
        This method computes pred from the inputs, given the other methods
        you've completed.

        Note that we are not applying a softmax to pred. The softmax will
        instead be done in the get_loss function, which improves efficiency
        because we can use torch.nn.functional.cross_entropy.
        Excluding the softmax in predictions won't change the expected
        transition.

        Args:
            word_id_batch:
                numpy.ndarray of dtype int64 and shape (B, n_word_features)
            tag_id_batch:
                numpy.ndarray of dtype int64 and shape (B, n_tag_features)
            deprel_id_batch:
                numpy.ndarray of dtype int64 and shape (B, n_deprel_features)
        Returns:
            pred: tf.Tensor of shape (batch_size, n_classes)

        - Given the concatenated embedding input x, complete the calculation of
          the forward pass as specified above. You will want to use the
          torch.nn.functional.relu and torch.nn.functional.dropout functions.
          This file already imports torch.nn.functional as F, so the function
          calls will be to F.relu and F.dropout.
        - Remember that dropout behaves differently when training vs. when
          evaluating. The F.dropout function reflects this. You can use
          self.training to indicate whether or not the model is currently being
          trained.
        """
        x = self.get_concat_embeddings(torch.tensor(word_id_batch),
                                       torch.tensor(tag_id_batch),
                                       torch.tensor(deprel_id_batch))

        # *** BEGIN YOUR CODE ***
        h = F.relu(torch.mm(x, self.W_h) + self.b_h)
        h_drop = F.dropout(h, self.config.dropout, training=self.training)
        pred = torch.mm(h_drop, self.W_o) + self.b_o
        # *** END YOUR CODE ***
        return pred

    def get_loss(self, prediction_batch, class_batch):
        """Calculate the value of the loss function

        In this case we are using cross entropy loss. The loss will be averaged
        over all examples in the current minibatch. Use F.cross_entropy to
        simplify your implementation.

        Args:
            prediction_batch:
                A tensor of shape (batch_size, n_classes) containing the
                logits of the neural network, i.e., the output of the neural
                network before the softmax activation.
            class_batch:
                A tensor of shape (batch_size,) containing the ground truth
                class labels.
        Returns:
            loss: A 0d tensor (scalar)
        """
        # *** BEGIN YOUR CODE ***
        loss = F.cross_entropy(prediction_batch, class_batch)
        # *** END YOUR CODE ***
        return loss

    def add_optimizer(self):
        """Sets up the optimizer.

        Creates an optimizer sets it as an attribute for this class.
        variables. The Op returned by this function is what must be
        passed to the `sess.run()` call to cause the model to train.

        - Use torch.optim.Adam for this model.
        - You will need to specify which parameters are to be optimized. For
          our model, that would be the embedding matrices and the layer weights
          and biases.
        - Assign the optimizer instance to self.optimizer. As above, don't
          change the attribute name!
        """
        # *** BEGIN YOUR CODE ***
        params_dicts = [{'params': self.word_embeddings, 'lr': self.config.lr, 'weight_decay': 0},
                       {'params': self.tag_embeddings, 'lr': self.config.lr, 'weight_decay': 0},
                       {'params': self.deprel_embeddings, 'lr': self.config.lr, 'weight_decay': 0},
                       {'params': self.W_h, 'lr': self.config.lr, 'weight_decay': 0.00001},
                       {'params': self.b_h, 'lr': self.config.lr, 'weight_decay': 0},
                       {'params': self.W_o, 'lr': self.config.lr, 'weight_decay': 0.00001},
                       {'params': self.b_o, 'lr': self.config.lr, 'weight_decay': 0}]
        optimizer = torch.optim.Adam(params_dicts)
        self.optimizer = optimizer
        # *** END YOUR CODE ***

    def _fit_batch(self, word_id_batch, tag_id_batch, deprel_id_batch,
                   class_batch):
        self.optimizer.zero_grad()
        pred_batch = self(word_id_batch, tag_id_batch, deprel_id_batch)
        loss = self.get_loss(pred_batch, torch.tensor(class_batch).argmax(-1))
        loss.backward()

        self.optimizer.step()

        return loss

    def fit_epoch(self, train_data, epoch, trn_progbar, batch_size=None):
        """Fit on training data for an epoch"""
        self.train()
        desc = 'Epoch %d/%d' % (epoch + 1, self.config.n_epochs)
        total = len(train_data) * batch_size if batch_size else len(train_data)
        bar_fmt = '{l_bar}{bar}| [{elapsed}<{remaining}{postfix}]'
        with tqdm(desc=desc, total=total, leave=False, miniters=1, unit='ex',
                  unit_scale=True, bar_format=bar_fmt, position=1) as progbar:
            trn_loss = 0
            trn_done = 0
            for ((word_id_batch, tag_id_batch, deprel_id_batch),
                 class_batch) in train_data:
                loss = self._fit_batch(word_id_batch, tag_id_batch,
                                       deprel_id_batch, class_batch)
                trn_loss += loss.item() * word_id_batch.shape[0]
                trn_done += word_id_batch.shape[0]
                progbar.set_postfix({'loss': '%.3g' % (trn_loss / trn_done)})
                progbar.update(word_id_batch.shape[0])
                trn_progbar.update(word_id_batch.shape[0] / total)
        return trn_loss / trn_done

    def predict(self, partial_parses):
        """Use this model to predict the next transitions/deprels of pps"""
        self.eval()
        feats = self.transducer.pps2feats(partial_parses)
        td_vecs = self(*feats).cpu().detach().numpy()
        preds = [
            self.transducer.td_vec2trans_deprel(td_vec) for td_vec in td_vecs]
        return preds

    def evaluate(self, sentences, ex_arcs):
        """LAS on either training or test sets"""
        act_arcs = minibatch_parse(sentences, self, self.config.batch_size)
        ex_arcs = tuple([(a[0], a[1],
                          self.transducer.id2deprel[a[2]]) for a in pp]
                        for pp in ex_arcs)
        stdout.flush()
        return score_arcs(act_arcs, ex_arcs)

    def __init__(self, transducer, config, word_embeddings):
        self.transducer = transducer
        self.config = config

        super().__init__()

        self.create_embeddings(word_embeddings)
        self.create_weights_biases()

        self.add_optimizer()


def main(debug):
    """Main function

    Args:
    debug :
        whether to use a fraction of the data. Make sure to set to False
        when you're ready to train your model for real!
    """
    print(80 * "=")
    print("INITIALIZING")
    print(80 * "=")
    torch.manual_seed(1234)
    if torch.cuda.is_available():
        torch.set_default_tensor_type(torch.cuda.FloatTensor)
        torch.cuda.manual_seed_all(1234)
        print('Running on GPU: {}.'.format(torch.cuda.get_device_name()))
    else:
        print('Running on CPU.')
    config = Config()
    data = load_and_preprocess_data(max_batch_size=config.batch_size,
                                    transition_cache=0 if debug else None)
    transducer, word_embeddings, train_data = data[:3]
    dev_sents, dev_arcs = data[3:5]
    test_sents, test_arcs = data[5:]
    config.n_word_ids = len(transducer.id2word) + 1  # plus null
    config.n_tag_ids = len(transducer.id2tag) + 1
    config.n_deprel_ids = len(transducer.id2deprel) + 1
    config.embed_size = word_embeddings.shape[1]
    for (word_batch, tag_batch, deprel_batch), td_batch in \
            train_data.get_iterator(shuffled=False):
        config.n_word_features = word_batch.shape[-1]
        config.n_tag_features = tag_batch.shape[-1]
        config.n_deprel_features = deprel_batch.shape[-1]
        config.n_classes = td_batch.shape[-1]
        break
    print('# word features: {}'.format(config.n_word_features))
    print('# tag features: {}'.format(config.n_tag_features))
    print('# deprel features: {}'.format(config.n_deprel_features))
    print('# classes: {}'.format(config.n_classes))
    if debug:
        dev_sents = dev_sents[:500]
        dev_arcs = dev_arcs[:500]
        test_sents = test_sents[:500]
        test_arcs = test_arcs[:500]

    print(80 * "=")
    print("TRAINING")
    print(80 * "=")
    weights_file = Path('weights.pt')
    i = 1
    if not debug:
        while weights_file.exists():
            i += 1
            weights_file = Path('weights%d.pt' % i)
        print('Best weights will be saved to:', weights_file)
    model = ParserModel(transducer, config, word_embeddings)
    if torch.cuda.is_available():
        model = model.cuda()
    best_las = 0.
    trnbar_fmt = '{l_bar}{bar}| [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
    with tqdm(desc='Training', total=config.n_epochs, leave=False,
              unit='epoch', position=0, bar_format=trnbar_fmt) as progbar:
        for epoch in range(config.n_epochs):
            if debug:
                trn_loss = model.fit_epoch(list(islice(train_data, 32)), epoch,
                                           progbar, config.batch_size)
            else:
                trn_loss = model.fit_epoch(train_data, epoch, progbar)
            tqdm.write('Epoch {:>2} training loss: {:.3g}'.format(epoch + 1,
                                                                  trn_loss))
            stdout.flush()
            dev_las, dev_uas = model.evaluate(dev_sents, dev_arcs)
            best = dev_las > best_las
            if best:
                best_las = dev_las
                if not debug:
                    torch.save(model.state_dict(), str(weights_file))
            tqdm.write('         validation LAS: {:.3f}{} UAS: {:.3f}'.format(
                dev_las, ' (BEST!)' if best else '        ', dev_uas))
    if not debug:
        print()
        print(80 * "=")
        print("TESTING")
        print(80 * "=")
        print("Restoring the best model weights found on the dev set.")
        model.load_state_dict(torch.load(str(weights_file)))
        stdout.flush()
        las, uas = model.evaluate(test_sents, test_arcs)
        if las:
            print('Test LAS: {:.3f}'.format(las), end='       ')
        print('UAS: {:.3f}'.format(uas))
        print("Done.")
    return 0


if __name__ == '__main__':
    main(False)
