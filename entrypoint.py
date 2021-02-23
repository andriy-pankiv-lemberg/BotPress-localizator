from logging import config

from app.configs import SupervisorConfig, LoggingConfig
from app.process.bot_reader import CoughSupervisor


def main():
    LoggingConfig.create_folder_if_doesnt_exist(LoggingConfig.LOG_PATH)
    config.dictConfig(LoggingConfig.LOG_API_CONF)
    cough_supervisor = CoughSupervisor(SupervisorConfig)
    cough_supervisor.run_tests()


if __name__ == "__main__":
    main()
