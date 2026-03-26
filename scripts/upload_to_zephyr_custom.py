import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"ERROR: Missing required environment variable: {name}", file=sys.stderr)
        sys.exit(1)
    return value


def junit_status(testcase: ET.Element) -> str:
    """
    Map JUnit testcase outcome to Zephyr result values.
    """
    if testcase.find("failure") is not None or testcase.find("error") is not None:
        return "Failed"
    if testcase.find("skipped") is not None:
        return "Not Executed"
    return "Passed"


def extract_property(testcase: ET.Element, property_name: str) -> Optional[str]:
    properties = testcase.find("properties")
    if properties is None:
        return None

    for prop in properties.findall("property"):
        if prop.get("name") == property_name:
            return prop.get("value")
    return None


def build_source_name(testcase: ET.Element) -> str:
    classname = testcase.get("classname", "").strip()
    name = testcase.get("name", "").strip()

    if classname and name:
        return f"{classname}.{name}"
    return name or classname or "unknown_test"


def build_execution(testcase: ET.Element) -> Optional[Dict[str, Any]]:
    test_key = extract_property(testcase, "test_key")
    if not test_key:
        return None

    execution: Dict[str, Any] = {
        "source": build_source_name(testcase),
        "result": junit_status(testcase),
        "testCase": {
            "key": test_key,
        },
    }

    test_time = testcase.get("time")
    if test_time:
        try:
            execution["executionTime"] = int(float(test_time) * 1000)
        except ValueError:
            pass

    comment_parts: List[str] = []

    environment = extract_property(testcase, "environment") or os.getenv("TEST_ENV")
    # if environment:
    #     comment_parts.append(f"<b>Environment:</b> {environment}")

    browser = extract_property(testcase, "browser")
    if browser:
        comment_parts.append(f"Browser: {browser}")

    failure = testcase.find("failure")
    error = testcase.find("error")
    skipped = testcase.find("skipped")

    if failure is not None:
        failure_message = format_failure_message((failure.get("message") or "").strip())

        if failure_message:
            comment_parts.append(f"<b>Failure:</b> {failure_message}")
        else:
            comment_parts.append("<b>Failure:</b> Test failed")

    elif error is not None:
        error_message = format_failure_message((error.get("message") or "").strip())

        if error_message:
            comment_parts.append(f"<b>Error:</b> {error_message}")
        else:
            comment_parts.append("<b>Error: Test errored")

    elif skipped is not None:
        skipped_message = (skipped.get("message") or "").strip()
        if skipped_message:
            comment_parts.append(f"Skipped: {skipped_message}")
        else:
            comment_parts.append("Skipped")

    else:
        comment_parts.append("<b>Result:</b> Passed")

    github_run_url = build_github_run_url()
    if github_run_url:
        comment_parts.append(f"<b>GitHub Run:</b> {github_run_url}")

    artifact_note = os.getenv("ZEPHYR_ARTIFACT_NOTE", "").strip()
    if artifact_note:
        comment_parts.append(f"<b>Artifacts:</b> {artifact_note}")

    if comment_parts:
        execution["comment"] = "<br><br>".join(comment_parts)

    return execution


def parse_junit_xml(results_file: Path) -> List[Dict[str, Any]]:
    tree = ET.parse(results_file)
    root = tree.getroot()

    executions: List[Dict[str, Any]] = []
    for testcase in root.findall(".//testcase"):
        execution = build_execution(testcase)
        if execution:
            executions.append(execution)

    return executions


def build_payload(results_file: Path) -> Dict[str, Any]:
    executions = parse_junit_xml(results_file)
    if not executions:
        print(
            "ERROR: No mapped test cases found in results XML. "
            "Make sure your tests write <property name='test_key' value='QAVM-T#' />.",
            file=sys.stderr,
        )
        sys.exit(1)

    return {
        "version": 1,
        "executions": executions,
    }


def map_status(result: str) -> str:
    """
    Map custom automation result to Zephyr test execution status.
    """
    normalized = result.strip().lower()

    if normalized == "passed":
        return "Pass"
    if normalized == "failed":
        return "Fail"
    if normalized == "not executed":
        return "Blocked"

    return "Fail"


def create_test_cycle(token: str, project_key: str) -> str:
    """
    Create a new Zephyr test cycle for this run and return the cycle key.
    """
    url = "https://api.zephyrscale.smartbear.com/v2/testcycles"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    cycle_name = os.getenv("ZEPHYR_TEST_CYCLE_NAME", "Automated Build")
    description = os.getenv("ZEPHYR_TEST_CYCLE_DESCRIPTION", "").strip()

    body: Dict[str, Any] = {
        "projectKey": project_key,
        "name": cycle_name,
    }

    if description:
        body["description"] = description

    folder_id = os.getenv("ZEPHYR_TEST_CYCLE_FOLDER_ID", "").strip()
    if folder_id:
        try:
            body["folderId"] = int(folder_id)
        except ValueError:
            print(
                f"WARNING: Invalid ZEPHYR_TEST_CYCLE_FOLDER_ID: {folder_id}. Ignoring.",
                file=sys.stderr,
            )

    jira_project_version = os.getenv("ZEPHYR_JIRA_PROJECT_VERSION", "").strip()
    if jira_project_version:
        try:
            body["jiraProjectVersion"] = int(jira_project_version)
        except ValueError:
            print(
                f"WARNING: Invalid ZEPHYR_JIRA_PROJECT_VERSION: {jira_project_version}. Ignoring.",
                file=sys.stderr,
            )

    response = requests.post(url, headers=headers, json=body, timeout=120)

    print(f"Create cycle -> HTTP {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

    if response.status_code >= 400:
        sys.exit(1)

    response_json = response.json()
    cycle_key = response_json.get("key")
    if not cycle_key:
        print("ERROR: Zephyr did not return a test cycle key.", file=sys.stderr)
        sys.exit(1)

    return cycle_key

def create_test_execution(
    execution: Dict[str, Any],
    cycle_key: str,
    token: str,
    project_key: str,
) -> None:
    """
    Create a Zephyr test execution directly so comment/environment/time
    are written to the execution record.
    """
    url = "https://api.zephyrscale.smartbear.com/v2/testexecutions"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    body: Dict[str, Any] = {
        "projectKey": project_key,
        "testCaseKey": execution["testCase"]["key"],
        "testCycleKey": cycle_key,
        "statusName": map_status(execution["result"]),
        "executionTime": execution.get("executionTime", 0),
        "comment": execution.get("comment", ""),
    }

    environment_name = os.getenv("TEST_ENV", "").strip()
    if environment_name:
        body["environmentName"] = environment_name

    response = requests.post(url, headers=headers, json=body, timeout=120)

    print(f"Create execution for {body['testCaseKey']} -> HTTP {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

    if response.status_code >= 400:
        sys.exit(1)

def format_failure_message(message: str) -> str:
    """
    Format flattened pytest/playwright failure text into a cleaner Zephyr comment.
    """
    if not message:
        return ""

    # Normalize whitespace first
    formatted = " ".join(message.strip().split())

    # Insert line breaks before common sections
    formatted = re.sub(r"\s+Actual value:", r"<br><b>Actual value:</b>", formatted)
    formatted = re.sub(r"\s+Error:", r"<br><b>Error:</b>", formatted)
    formatted = re.sub(r"\s+Call log:", r"<br><b>Call log:</b>", formatted)

    # Insert line breaks before common bullet items in Playwright call logs
    formatted = re.sub(r'\s+-\s+Expect\b', r'<br>- Expect', formatted)
    formatted = re.sub(r'\s+-\s+waiting for\b', r'<br>- waiting for', formatted)
    formatted = re.sub(r'\s+-\s+Locator resolved to\b', r'<br>- Locator resolved to', formatted)
    formatted = re.sub(r'\s+-\s+unexpected value\b', r'<br>- unexpected value', formatted)

    return formatted

def build_github_run_url() -> str:
    server_url = os.getenv("GITHUB_SERVER_URL", "").strip()
    repository = os.getenv("GITHUB_REPOSITORY", "").strip()
    run_id = os.getenv("GITHUB_RUN_ID", "").strip()

    if server_url and repository and run_id:
        return f"{server_url}/{repository}/actions/runs/{run_id}"

    return ""

def main() -> None:
    token = require_env("ZEPHYR_TOKEN")
    project_key = require_env("ZEPHYR_PROJECT_KEY")

    results_file = Path(os.getenv("ZEPHYR_RESULTS_FILE", "reports/results.xml"))

    if not results_file.exists():
        print(f"ERROR: Results file not found: {results_file}", file=sys.stderr)
        sys.exit(1)

    payload = build_payload(results_file)

    # Save JSON locally for debugging / artifact upload
    payload_path = Path("reports/zephyrscale_payload.json")
    payload_path.parent.mkdir(parents=True, exist_ok=True)
    payload_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    cycle_key = create_test_cycle(token=token, project_key=project_key)

    print(f"Creating direct test execution(s) in cycle: {cycle_key}")

    for execution in payload["executions"]:
        create_test_execution(
            execution=execution,
            cycle_key=cycle_key,
            token=token,
            project_key=project_key,
        )

if __name__ == "__main__":
    main()