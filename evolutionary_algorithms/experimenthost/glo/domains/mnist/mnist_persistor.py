class MnistPersistor:
    def persist(self, tree, tree_idx, base_dir=None):

        if base_dir is None:
            base_dir = f"{os.getcwd()}/results/mnist/glo_mnist_{self.experiment_id}/candidates"

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        candidate_path = f"{base_dir}/tree_{tree_idx}"
        os.makedirs(candidate_path)
        stats = Statistics.statistics(tree)

        json_persistor = JsonPersistor("stats", candidate_path)
        json_persistor.persist(stats)

        # pickle_persistor = PicklePersistor("tree", candidate_path)
        # pickle_persistor.persist(tree)

    def persist_best_candidate(self, best_candidate):
        base_dir = f"{os.getcwd()}/results/mnist/glo_mnist_{self.experiment_id}/"
        stats = Statistics.statistics(best_candidate)

        json_persistor = JsonPersistor("stats", base_dir)
        json_persistor.persist(stats)