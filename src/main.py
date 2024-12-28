import threading
from config import Config
from scheduler import Scheduler
from github_client import GitHubClient
from notifier import Notifier
from report_generator import ReportGenerator
from subscription_manager import SubscriptionManager
from cli import CLI

def run_scheduler(scheduler):
    scheduler.start()

def main():
    # Initialize components
    config = Config()
    github_client = GitHubClient(config)
    notifier = Notifier(config.notification_settings)
    report_generator = ReportGenerator(config)
    subscription_manager = SubscriptionManager(config.subscriptions_file)
    
    # Setup and start scheduler
    scheduler = Scheduler(
        github_client=github_client,
        notifier=notifier,
        report_generator=report_generator,
        subscription_manager=subscription_manager,
        interval=config.update_interval
    )
    
    scheduler_thread = threading.Thread(target=run_scheduler, args=(scheduler,))
    scheduler_thread.daemon = True
    scheduler_thread.start()

    # Start CLI
    cli = CLI(
        github_client=github_client,
        subscription_manager=subscription_manager,
        report_generator=report_generator,
        config=config
    )
    cli.run()

if __name__ == "__main__":
    main()
