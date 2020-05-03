import tensorflow as tf
import copy
from bert import modeling,optimization,tokenization

class BertPredictor(object):
    """BERT model ("Bidirectional Encoder Representations from Transformers") for classification


    """

    def __init__(self,
                 config,
                 use_one_hot_embeddings=True,
                 num_labels=2,
                 max_seq_length=128):
        """Constructor for BertModel.

        Args:
          config: `BertConfig` instance.
          is_training: bool. true for training model, false for eval model. Controls
            whether dropout will be applied.
          input_ids: int32 Tensor of shape [batch_size, seq_length].
          input_mask: (optional) int32 Tensor of shape [batch_size, seq_length].
          token_type_ids: (optional) int32 Tensor of shape [batch_size, seq_length].
          use_one_hot_embeddings: (optional) bool. Whether to use one-hot word
            embeddings or tf.embedding_lookup() for the word embeddings. On the TPU,
            it is much faster if this is True, on the CPU or GPU, it is faster if
            this is False.
          scope: (optional) variable scope. Defaults to "bert".

        Raises:
          ValueError: The config is invalid or one of the input tensor shapes
            is invalid.
        """
        self.input_ids = tf.placeholder(dtype=tf.int32, shape=(None, max_seq_length))
        self.input_mask = tf.placeholder(dtype=tf.int8, shape=(None, max_seq_length))

        config = copy.deepcopy(config)

        input_shape = modeling.get_shape_list(self.input_ids, expected_rank=2)
        batch_size = input_shape[0]
        seq_length = input_shape[1]

        token_type_ids = tf.zeros(shape=[batch_size, seq_length], dtype=tf.int32)

        with tf.variable_scope("bert", reuse=tf.AUTO_REUSE):
            with tf.variable_scope("embeddings", reuse=tf.AUTO_REUSE):
                # Perform embedding lookup on the word ids.
                (self.embedding_output, self.embedding_table) = modeling.embedding_lookup(
                    input_ids=self.input_ids,
                    vocab_size=config.vocab_size,
                    embedding_size=config.hidden_size,
                    initializer_range=config.initializer_range,
                    word_embedding_name="word_embeddings",
                    use_one_hot_embeddings=use_one_hot_embeddings)

                # Add positional embeddings and token type embeddings, then layer
                # normalize and perform dropout.
                self.embedding_output = modeling.embedding_postprocessor(
                    input_tensor=self.embedding_output,
                    use_token_type=True,
                    token_type_ids=token_type_ids,
                    token_type_vocab_size=config.type_vocab_size,
                    token_type_embedding_name="token_type_embeddings",
                    use_position_embeddings=True,
                    position_embedding_name="position_embeddings",
                    initializer_range=config.initializer_range,
                    max_position_embeddings=config.max_position_embeddings,
                    dropout_prob=config.hidden_dropout_prob)

            with tf.variable_scope("encoder", reuse=tf.AUTO_REUSE):
                # This converts a 2D mask of shape [batch_size, seq_length] to a 3D
                # mask of shape [batch_size, seq_length, seq_length] which is used
                # for the attention scores.
                attention_mask = modeling.create_attention_mask_from_input_mask(
                    self.input_ids, self.input_mask)

                # Run the stacked transformer.
                # `sequence_output` shape = [batch_size, seq_length, hidden_size].
                self.all_encoder_layers = modeling.transformer_model(
                    input_tensor=self.embedding_output,
                    attention_mask=attention_mask,
                    hidden_size=config.hidden_size,
                    num_hidden_layers=config.num_hidden_layers,
                    num_attention_heads=config.num_attention_heads,
                    intermediate_size=config.intermediate_size,
                    intermediate_act_fn=modeling.get_activation(config.hidden_act),
                    hidden_dropout_prob=config.hidden_dropout_prob,
                    attention_probs_dropout_prob=config.attention_probs_dropout_prob,
                    initializer_range=config.initializer_range,
                    do_return_all_layers=True)

            self.sequence_output = self.all_encoder_layers[-1]
            # The "pooler" converts the encoded sequence tensor of shape
            # [batch_size, seq_length, hidden_size] to a tensor of shape
            # [batch_size, hidden_size]. This is necessary for segment-level
            # (or segment-pair-level) classification tasks where we need a fixed
            # dimensional representation of the segment.
            with tf.variable_scope("pooler", reuse=tf.AUTO_REUSE):
                # We "pool" the model by simply taking the hidden state corresponding
                # to the first token. We assume that this has been pre-trained
                first_token_tensor = tf.squeeze(self.sequence_output[:, 0:1, :], axis=1)
                self.pooled_output = tf.layers.dense(
                    first_token_tensor,
                    config.hidden_size,
                    activation=tf.tanh,
                    kernel_initializer=modeling.create_initializer(config.initializer_range))

        # define output_weights and output_bias
        hidden_size = self.pooled_output.shape[-1].value
        with tf.variable_scope("", reuse=tf.AUTO_REUSE):
            self.output_weights = tf.get_variable(
                "output_weights", [num_labels, hidden_size],
                initializer=tf.truncated_normal_initializer(stddev=0.02))
            self.output_bias = tf.get_variable(
                "output_bias", [num_labels], initializer=tf.zeros_initializer())

    def predict(self):
        '''
            return probability tensor
        '''
        bert_output_layer = self.pooled_output
        logits = tf.matmul(bert_output_layer, self.output_weights, transpose_b=True)
        logits = tf.nn.bias_add(logits, self.output_bias)
        probabilities = tf.nn.softmax(logits, axis=-1)

        return probabilities

    def initialize_ckpt(self, checkpoint_path):
        # call this function to initialize weights from checkpoint
        tvars = tf.trainable_variables()
        (assignment_map, initialized_variable_names) = modeling.get_assignment_map_from_checkpoint(tvars,
                                                                                                   checkpoint_path)
        tf.train.init_from_checkpoint(checkpoint_path, assignment_map)
