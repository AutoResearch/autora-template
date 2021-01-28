from AER_experimentalist.experiment_environment.participant_in_silico import Participant_In_Silico
import torch
import torch.nn as nn
from graphviz import Digraph
import random
import numpy as np

class Exp_Learning_Model(nn.Module):
    def __init__(self, alpha=0.5):
        super(Exp_Learning_Model, self).__init__()

        self.alpha = alpha

    def forward(self, input):

        input = torch.Tensor(input)
        if len(input.shape) <= 1:
            input = input.view(1, len(input))

        # convert inputs
        learning_trial = torch.zeros(input.shape[0], 1)
        P_initial = torch.zeros(input.shape[0], 1)
        P_asymptotic = torch.zeros(input.shape[0], 1)

        learning_trial[:, 0] = input[:, 0]
        P_initial[:, 0] = input[:, 1]
        P_asymptotic[:, 0] = input[:, 2]

        output = P_asymptotic - (P_asymptotic - P_initial) * torch.exp(- self.alpha * learning_trial)

        return output

class Participant_Exp_Learning(Participant_In_Silico):

    # initializes participant
    def __init__(self, alpha=0.5):
        super(Participant_Exp_Learning, self).__init__()

        self.learning_trial = torch.ones(1, 1)
        self.P_initial = torch.ones(1, 1)
        self.P_asymptotic = torch.zeros(1, 1)

        self.output = torch.zeros(1, 1)
        self.output_sampled = torch.zeros(1, 1)
        self.model = Exp_Learning_Model(alpha=alpha)

    # read value from participant
    def get_value(self, variable_name):

        if variable_name is "learning_trial":
            return self.learning_trial[0, 0].numpy()

        elif variable_name is "P_initial":
            return self.P_initial[0, 1].numpy()

        elif variable_name is "P_asymptotic":
            return self.P_initial[0, 1].numpy()

        elif variable_name is "learning_performance_sample":
            return self.output_sample[0, 0].numpy()

        elif variable_name is "learning_performance":
            return self.output[0, 0].numpy()

        raise Exception('Could not get value from Exponential Learning Participant. Variable name "' + variable_name + '" not found.')

    # assign value to participant
    def set_value(self, variable_name, value):

        if variable_name is "learning_trial":
            self.learning_trial[0, 0] = value

        elif variable_name is "P_initial":
            self.P_initial[0, 0] = value

        elif variable_name is "P_asymptotic":
            self.P_asymptotic[0, 0] = value

        elif variable_name is "learning_performance_sample":
            self.learning_performance_sample[0, 0] = value

        elif variable_name is "learning_performance":
            self.learning_performance[0, 0] = value

        else:
            raise Exception('Could not set value for Exponential Learning Participant. Variable name "' + variable_name + '" not found.')

    def execute(self):

        input = torch.zeros(1, 3)
        input[0, 0] = self.learning_trial
        input[0, 1] = self.P_initial
        input[0, 2] = self.P_asymptotic

        # compute regular output
        self.output = self.model(input).detach()

        # compute sample
        sample = random.uniform(0, 1)
        if sample < self.output:
            self.output_sampled[0] = 1
        else:
            self.output_sampled[0] = 0

    def compute_BIC(self, object_of_study, num_params = None):

        (input, target) = object_of_study.get_dataset()

        input_full = torch.zeros(input.shape[0], 3)
        input_full[:, 0] = self.learning_trial[0, 0]
        input_full[:, 1] = self.P_initial[0, 0]
        input_full[:, 2] = self.P_asymptotic[0, 0]

        for idx, IV in enumerate(object_of_study.independent_variables):
            variable_name = IV.get_name()
            if variable_name is "learning_trial":
                input_full[:, 0] = input[:, idx]
            if variable_name is "P_initial":
                input_full[:, 1] = input[:, idx]
            if variable_name is "P_asymptotic":
                input_full[:, 2] = input[:, idx]

        output_fnc = nn.Identity
        return super(Participant_Exp_Learning, self).compute_BIC(input_full, target, output_fnc, num_params)

    def graph_simple(self, filepath):
        raise Exception("Not implemented")


def run_exp(model, P_initial_list, P_asymptotic_list, learning_trials_list):
    output = list()

    for P_initial, P_asymptotic in zip(P_initial_list, P_asymptotic_list):
        output.append(list())
        for trial in learning_trials_list:
            input = [trial, P_initial, P_asymptotic]
            output[-1].append(model(input))


    return output


def plot_learning_curve(model, P_initial=(0, 0.25, 0.25), P_asymptotic=(1, 1, 0.75), learning_trials=range(10)):

    output = run_exp(model, P_initial, P_asymptotic, learning_trials)

    # collect plot data
    x1_data = learning_trials
    x2_data = learning_trials
    x3_data = learning_trials
    y1_data = output[0]
    y2_data = output[1]
    y3_data = output[2]

    x_limit = [0, np.max(learning_trials)]
    y_limit = [0, 1]
    x_label = "Trial"
    y_label = "P(correct)"
    legend = list()
    for P_init, P_asymp in zip(P_initial, P_asymptotic):
        legend.append('P_0 = ' + str(P_init) + ', P_inf = ' + str(P_asymp))

    # plot
    import matplotlib.pyplot as plt
    plt.plot(x1_data, y1_data, '.-', label=legend[0])
    plt.plot(x2_data, y2_data, '.-', label=legend[1])
    plt.plot(x3_data, y3_data, '.-', label=legend[2])
    plt.xlim(x_limit)
    plt.ylim(y_limit)
    plt.xlabel(x_label, fontsize="large")
    plt.ylabel(y_label, fontsize="large")
    plt.legend(loc=4, fontsize="large")
    plt.show()

# model = Exp_Learning_Model()
# plot_learning_curve(model)