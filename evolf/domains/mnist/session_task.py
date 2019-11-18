import os
import sys

sys.path.append(os.getcwd())
from evolf.framework.domain.argument_parser import ArgumentParser

if __name__ == "__main__":
    ArgumentParser.add_parser()

    studio_file_path = os.path.join(os.getcwd(), "temp/studio/studio_config.yaml")
    command = f"studio run --force-git --config={studio_file_path} evolf/domains/mnist/mnist.py"
    os.system(command)