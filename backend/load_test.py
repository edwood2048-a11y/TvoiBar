import asyncio
import aiohttp
import time

async def create_event(session, i):
    data = {
        "title": f"Load Test Event {i}",
        "description": "Load test description",
        "latitude": 50.4501 + i * 0.001,
        "longitude": 30.5234 + i * 0.001
    }
    async with session.post("http://127.0.0.1:8000/api/v1/events/", json=data, params={"creator_id": 1}) as response:
        return response.status

async def get_events(session):
    async with session.get("http://127.0.0.1:8000/api/v1/events/") as response:
        return response.status, len(await response.json())

async def main():
    # Start backend if not running
    print("Starting load test... Ensure backend is running on http://127.0.0.1:8000")

    async with aiohttp.ClientSession() as session:
        # Test creating 100 events
        print("Creating 100 events...")
        start = time.time()
        tasks = [create_event(session, i) for i in range(100)]
        results = await asyncio.gather(*tasks)
        end = time.time()
        success_count = sum(1 for r in results if r == 200)
        print(f"Created {success_count}/100 events in {end - start:.2f}s")

        # Test reading events multiple times
        print("Reading events 50 times...")
        start = time.time()
        tasks = [get_events(session) for _ in range(50)]
        results = await asyncio.gather(*tasks)
        end = time.time()
        avg_events = sum(count for _, count in results) / len(results)
        print(f"Average events per read: {avg_events}, time: {end - start:.2f}s")

        # Check final count
        async with session.get("http://127.0.0.1:8000/api/v1/events/") as response:
            events = await response.json()
            print(f"Total events in DB: {len(events)}")

if __name__ == "__main__":
    asyncio.run(main())