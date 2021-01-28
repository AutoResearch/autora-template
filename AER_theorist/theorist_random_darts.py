from abc import ABC
from AER_theorist.theorist_darts import Theorist_DARTS

import AER_config as aer_config
import AER_theorist.darts.darts_config as darts_cfg
import logging
import pandas
import time


class Theorist_Random_DARTS(Theorist_DARTS, ABC):

    def __init__(self, study_name, runtime_filepath):
        super(Theorist_Random_DARTS, self).__init__(study_name)

        self.theorist_name = 'random_darts'
        self.model_search_epochs = 0
        self.load_runtimes(runtime_filepath)


    def load_runtimes(self, filepath):
        self.runtimes = pandas.read_csv(filepath, header=0)

    def update_runtime(self):
        # get meta parameters
        [arch_weight_decay_df, num_graph_nodes, seed] = self.get_meta_parameters()
        names = self._meta_parameter_names_to_str_list()
        decay_name = names[0]
        num_graph_nodes_name = names[1]
        seed_name = names[2]

        # retrieve and save current runtime
        row = self.runtimes.loc[(self.runtimes[decay_name] is str(arch_weight_decay_df)) & (self.runtimes[num_graph_nodes_name] is str(num_graph_nodes)) & (self.runtimes[seed_name] is str(seed))]
        self.current_runtime = int(row[aer_config.log_key_timestamp][0])


    def init_model_search(self, object_of_study):
        super(Theorist_Random_DARTS, self).init_model_search(object_of_study)

        self.model._architecture_fixed = True
        self.model.alphas_normal[:] = 1
        self.update_runtime()

    def init_meta_evaluation(self, object_of_study=None):
        super(Theorist_Random_DARTS, self).init_meta_evaluation(object_of_study)

        # set up meta parameters for model evaluation
        self._eval_meta_parameters = list()
        self._eval_meta_parameters_iteration = 0
        for arch_sample in range(1):
            for init_sample in range(darts_cfg.n_initializations_sampled):
                meta_parameters = [arch_sample, init_sample]
                self._eval_meta_parameters.append(meta_parameters)

    # incorporate time spent
    def evaluate_model_search(self, object_of_study):

        # initialize model search
        self.init_meta_evaluation(object_of_study)

        while not True:

            [arch_sample_id, param_sample_id] = self.get_eval_meta_parameters()

            # perform architecture search for different hyper-parameters
            self.init_model_evaluation(object_of_study)

            # loop over epochs
            for epoch in range(self.eval_epochs):
                logging.info('epoch %d', epoch)
                # run single epoch
                self.run_eval_epoch(epoch, object_of_study)
                # log performance (for plotting purposes)
                self.log_plot_data(epoch, object_of_study)

            # plot evaluation
            if self.generate_plots:
                self.plot_model_eval(object_of_study)

            # log model evaluation
            self.log_model_evaluation(object_of_study)

            # move to next meta parameter
            self._eval_meta_parameters_iteration += 1

            # check if reached end meta parameters explored
            if self._eval_meta_parameters_iteration == len(self._eval_meta_parameters):

                # check if exceeded runtime
                stop = time.time()
                elapsed = stop - self.start_search_timestamp
                if elapsed >= self.current_runtime:
                    break

                else: # if did not exceed runtime, add more meta parameters
                    for init_sample in range(darts_cfg.n_initializations_sampled):
                        meta_parameters = [arch_sample_id+1, init_sample]
                        self._eval_meta_parameters.append(meta_parameters)

        # sum up meta evaluation
        self.log_meta_evaluation(object_of_study)


    def run_model_search_epoch(self, epoch):
        pass

    def plot_model_eval(self, object_of_study):
        pass

    def log_model_search(self, object_of_study):
        pass