from framework.domain.get_default_config import GetDefaultConfig
from servicecommon.utils.overlayer import Overlayer


class ConfigHandler:

    def __init__(self, config):
        self.config = config

    def overlay_config(self):
        """""
        Overlay the config with the config default config
        to fill in missing parameters
        """""
        default_config = GetDefaultConfig.get_default_config()
        config = Overlayer.overlay_configs(default_config,
                                           self.config)
        return config

    def generate_evaluator_config(self, domain_config, evaluator_config):
        """
        This function adds the required params needed
        over from the domain_config and the required paths
        :return evaluator_config: The overlayed evaluator_config
        """
        # Get the Original Paths
        data_config = domain_config["data_config"]
        model_config = domain_config["model_config"]

        # Copy these to the evaluator config
        evaluator_config["data_config"] = data_config
        evaluator_config["model_config"] = model_config

        # Add the paths to save the files
        evaluator_config["model_save_folder"] = ".temp/model"
        evaluator_config["data_save_folder"] = ".temp/data"

        return evaluator_config
