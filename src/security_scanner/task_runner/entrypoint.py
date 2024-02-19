import asyncio
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "security_scanner.settings")

import django
django.setup()

from data_loss_protection.task import dlp_scan
from task_runner.manager import Manager


async def main():
    manager = Manager(
        tasks={
            'DLP_scan': dlp_scan,
        }
    )

    await manager.main()


if __name__ == '__main__':
    asyncio.run(main())
