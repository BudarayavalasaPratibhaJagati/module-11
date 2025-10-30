import subprocess, time, sys, requests
import pytest
from playwright.sync_api import Page, expect
SERVER = "http://127.0.0.1:8000"

@pytest.fixture(scope="session", autouse=True)
def run_server():
    try:
        requests.get(SERVER + "/health", timeout=1)
        yield
        return
    except Exception:
        pass
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    for _ in range(50):
        try:
            time.sleep(0.1)
            requests.get(SERVER + "/health", timeout=1)
            break
        except Exception:
            continue
    yield
    proc.terminate()

def test_happy_path(page: Page):
    page.goto(SERVER + "/")
    page.fill("#a", "6")
    page.fill("#b", "7")
    page.select_option("#op", "multiply")
    page.click("#go")
    expect(page.locator("#result")).to_have_text("Result = 42")
