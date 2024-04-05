def tanh(x):
    return np.tanh(x)


def tanh_grad(x):
    return 1 - np.tanh(x) ** 2


class NN():
    def __init__(self,architecture, learning_rate=0.1, activation=lambda x: x, activation_grad=lambda x: 1):
        '''This is a fully connected NN. The architecture is a list, 
        with each element specifying the number of nodes in each layer'''
        self.arch = architecture
        self.num_layers = len(self.arch) - 1
        self.activation = activation
        self.activation_grad = activation_grad
        self.lr = learning_rate
        self.init_weights()
        
        
    def init_weights(self):
        np.random.seed(0)
        self.weights = []
        self.biases= []
        for n in range(self.num_layers):
            self.weights.append(np.random.random((self.arch[n], self.arch[n+1])))
            self.biases.append(np.random.random((1, self.arch[n + 1])))

        
    def feed_forward(self, X):
        self.a_ns = []
        self.z_ns = []
        self.a_ns.append(X)
        for n in range(self.num_layers):
            z_n = np.dot(self.a_ns[-1], self.weights[n]) + self.biases[n]
            
            self.z_ns.append(z_n)
            self.a_ns.append(self.activation(z_n))

        return self.a_ns[-1]
            
    def loss_func(self, X, y):
        feed_forward = self.feed_forward(X)
        loss = np.mean((feed_forward - y) ** 2) * 0.5
        return loss
    
    
    def calc_layer_errors(self, X, y):
        feed_forward = self.feed_forward(X)

        self.layer_errors = []
        error_last_layer = (feed_forward - y) * self.activation_grad(self.z_ns[-1]) * 0.5
        self.layer_errors.append(error_last_layer)


        for i in range(self.num_layers - 2, -1, -1):
            error = self.activation_grad(self.z_ns[i]) * np.dot(self.layer_errors[-1], self.weights[i+1].T)
            self.layer_errors.insert(0, error)
        return self.layer_errors

    def calc_grads(self, X, y):
        self.calc_layer_errors(X, y)
        self.biases_grad, self.weights_grad = [], []
        
        for i in range(self.num_layers):
            if i == 0:
                wg = np.dot(X.T, self.layer_errors[i]) / len(X)
            else:
                wg = np.dot(self.a_ns[i].T, self.layer_errors[i]) / len(X)
            self.weights_grad.append(wg)
            
            bg = np.mean(self.layer_errors[i], axis=0, keepdims=True)
            self.biases_grad.append(bg)

            

        
    def back_prop(self, X, y):
        self.calc_grads(X, y)
        for i in range(self.num_layers):
            self.biases[i] -= self.lr * self.biases_grad[i]
            self.weights[i] -= self.lr * self.weights_grad[i]
    