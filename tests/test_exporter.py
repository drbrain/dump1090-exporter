import asyncio
from pathlib import Path
from typing import Optional

import asynctest
from aiohttp import ClientSession, web
from aioprometheus import REGISTRY

import dump1090exporter.exporter
import dump1090exporter.metrics
from dump1090exporter import Dump1090Exporter

GOLDEN_DATA_DIR = Path(__file__).parent / "golden-data"
AIRCRAFT_DATA_FILE = GOLDEN_DATA_DIR / "aircraft.json"
STATS_DATA_FILE = GOLDEN_DATA_DIR / "stats.json"
RECEIVER_DATA_FILE = GOLDEN_DATA_DIR / "receiver.json"
TEST_ORIGIN = (-34.928500, 138.600700)  # (lat, lon)


class Dump1090ServiceEmulator:
    """This class implements a HTTP server that emulates the dump1090 service"""

    def __init__(self):  # pylint: disable=missing-function-docstring
        self._runner = None  # type: Optional[web.AppRunner]
        self.url = None  # type: Optional[str]
        self.paths = {
            "/aircraft.json": AIRCRAFT_DATA_FILE,
            "/stats.json": STATS_DATA_FILE,
            "/receiver.json": RECEIVER_DATA_FILE,
        }

    async def handle_request(self, request):
        """Handle a HTTP request for a dump1090 resource"""
        if request.path not in self.paths:
            raise Exception(f"Unhandled path: {request.path}")

        data_file = self.paths[request.path]
        with data_file.open("rt") as f:
            content = f.read()
        return web.Response(status=200, body=content, content_type="application/json")

    async def start(self, addr="127.0.0.1", port=9999):
        """Start the dump1090 service emulator"""
        app = web.Application()
        app.add_routes(
            [web.get(request_path, self.handle_request) for request_path in self.paths]
        )
        self._runner = web.AppRunner(app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, addr, port)
        await site.start()
        self.url = site.name

    async def stop(self):
        """Stop the dump1090 service emulator"""
        await self._runner.cleanup()


class TestExporter(asynctest.TestCase):  # pylint: disable=missing-class-docstring
    def tearDown(self):
        REGISTRY.clear()

    async def test_exporter(self):
        """Check dump1090exporter application"""
        # Start a fake dump1090 service that the exporter can scrape
        ds = Dump1090ServiceEmulator()
        try:
            await ds.start()

            # Start the dump1090exporter
            de = Dump1090Exporter(resource_path=ds.url, origin=TEST_ORIGIN, port=9998)

            await de.start()
            await asyncio.sleep(0.3)

            # Scrape the dump1090exporter just as Prometheus would
            async with ClientSession() as session:
                async with session.get(de.svr.metrics_url, timeout=0.3) as resp:
                    if not resp.status == 200:
                        raise Exception(f"Fetch failed {resp.status}: {resp.url()}")
                    data = await resp.text()

            # Check that expected metrics are present in the response
            specs = dump1090exporter.metrics.Specs
            for _attr, prometheus_name, _doc in specs["aircraft"]:
                self.assertIn(f"{de.prefix}{prometheus_name}", data)
            for _group_name, group_metrics in specs["stats"].items():
                for (_type, _tp, _s_name, prometheus_name, _doc) in group_metrics:
                    self.assertIn(f"{de.prefix}{prometheus_name}", data)

            await de.stop()

            # check calling stop again does not raise errors
            await de.stop()

        finally:
            await ds.stop()
