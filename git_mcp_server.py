#!/usr/bin/env python3
"""
Git MCP Server (GitHub + GitLab + Local Git)
Model Context Protocol (MCP) server over stdio providing tools for interacting
with local Git repositories, GitHub API, and GitLab API.
"""

import sys
import json
import subprocess
import os
import urllib.request
import urllib.parse
import urllib.error

# Config defaults
DEFAULT_GITLAB_HOST = os.environ.get("GITLAB_URL", "https://git.ipoint.uz").rstrip("/")
DEFAULT_GITHUB_HOST = "https://api.github.com"

TOOLS = [
    {
        "name": "git_status",
        "description": "Get git status for a local repository directory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Absolute or relative path to local git repository directory."
                }
            },
            "required": ["repo_path"]
        }
    },
    {
        "name": "git_log",
        "description": "Get git commit history log for a local repository.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Path to local git repository directory."
                },
                "max_count": {
                    "type": "integer",
                    "description": "Maximum number of commits to return. Default is 10."
                }
            },
            "required": ["repo_path"]
        }
    },
    {
        "name": "git_diff",
        "description": "Get git diff for a local repository.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Path to local git repository directory."
                },
                "staged": {
                    "type": "boolean",
                    "description": "If true, show staged changes (--staged). Default is false."
                }
            },
            "required": ["repo_path"]
        }
    },
    {
        "name": "git_branch_list",
        "description": "List local and remote git branches.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Path to local git repository directory."
                }
            },
            "required": ["repo_path"]
        }
    },
    {
        "name": "git_commit_info",
        "description": "Get detailed commit information by commit hash.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "repo_path": {
                    "type": "string",
                    "description": "Path to local git repository directory."
                },
                "commit_hash": {
                    "type": "string",
                    "description": "Commit SHA or reference name."
                }
            },
            "required": ["repo_path", "commit_hash"]
        }
    },
    {
        "name": "github_api",
        "description": "Call GitHub REST API endpoints.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "endpoint": {
                    "type": "string",
                    "description": "API path endpoint, e.g. '/repos/owner/repo/pulls' or '/user'."
                },
                "method": {
                    "type": "string",
                    "description": "HTTP method (GET, POST, PUT, DELETE). Default is GET."
                },
                "token": {
                    "type": "string",
                    "description": "GitHub Personal Access Token (defaults to GITHUB_TOKEN or GH_TOKEN env vars if omitted)."
                },
                "params": {
                    "type": "object",
                    "description": "Query parameters or JSON request body."
                }
            },
            "required": ["endpoint"]
        }
    },
    {
        "name": "gitlab_api",
        "description": "Call GitLab REST API (v4) endpoints (supports custom GitLab host like git.ipoint.uz).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "endpoint": {
                    "type": "string",
                    "description": "GitLab API v4 endpoint path, e.g. '/projects', '/projects/123/merge_requests', '/user'."
                },
                "method": {
                    "type": "string",
                    "description": "HTTP method (GET, POST, PUT, DELETE). Default is GET."
                },
                "gitlab_url": {
                    "type": "string",
                    "description": "GitLab base URL. Defaults to GITLAB_URL env var or https://git.ipoint.uz."
                },
                "token": {
                    "type": "string",
                    "description": "GitLab Private Token / Personal Access Token (defaults to GITLAB_TOKEN or GL_TOKEN env vars if omitted)."
                },
                "params": {
                    "type": "object",
                    "description": "Query parameters or JSON body payload."
                }
            },
            "required": ["endpoint"]
        }
    }
]

def run_git_cmd(repo_path, args):
    if not os.path.exists(repo_path):
        return {"error": f"Repository path '{repo_path}' does not exist."}
    cmd = ["git", "-C", repo_path] + args
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode != 0:
            return {"error": res.stderr.strip() or f"Git command exited with code {res.returncode}"}
        return {"output": res.stdout.strip()}
    except Exception as e:
        return {"error": str(e)}

def http_request(url, method="GET", headers=None, data=None):
    headers = headers or {}
    req_data = None
    if data:
        if isinstance(data, dict) and method in ["POST", "PUT", "PATCH"]:
            req_data = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif isinstance(data, dict) and method == "GET":
            url += "?" + urllib.parse.urlencode(data)
    
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            try:
                return json.loads(body)
            except json.JSONDecodeError:
                return {"response_text": body}
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        return {"error": f"HTTP {e.code}: {e.reason}", "details": err_body}
    except Exception as e:
        return {"error": str(e)}

def execute_tool(name, arguments):
    if name == "git_status":
        repo_path = arguments.get("repo_path", ".")
        return run_git_cmd(repo_path, ["status"])
    elif name == "git_log":
        repo_path = arguments.get("repo_path", ".")
        max_count = arguments.get("max_count", 10)
        return run_git_cmd(repo_path, ["log", f"-n{max_count}", "--oneline", "--decorate"])
    elif name == "git_diff":
        repo_path = arguments.get("repo_path", ".")
        staged = arguments.get("staged", False)
        args = ["diff", "--staged"] if staged else ["diff"]
        return run_git_cmd(repo_path, args)
    elif name == "git_branch_list":
        repo_path = arguments.get("repo_path", ".")
        return run_git_cmd(repo_path, ["branch", "-a"])
    elif name == "git_commit_info":
        repo_path = arguments.get("repo_path", ".")
        commit_hash = arguments.get("commit_hash")
        return run_git_cmd(repo_path, ["show", commit_hash, "--stat"])
    elif name == "github_api":
        endpoint = arguments.get("endpoint", "").lstrip("/")
        method = arguments.get("method", "GET").upper()
        token = arguments.get("token") or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        params = arguments.get("params")
        url = f"{DEFAULT_GITHUB_HOST}/{endpoint}"
        headers = {"User-Agent": "Git-MCP-Server", "Accept": "application/vnd.github.v3+json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return http_request(url, method=method, headers=headers, data=params)
    elif name == "gitlab_api":
        endpoint = arguments.get("endpoint", "").lstrip("/")
        if not endpoint.startswith("api/v4"):
            endpoint = f"api/v4/{endpoint}"
        method = arguments.get("method", "GET").upper()
        host = arguments.get("gitlab_url") or DEFAULT_GITLAB_HOST
        token = arguments.get("token") or os.environ.get("GITLAB_TOKEN") or os.environ.get("GL_TOKEN")
        params = arguments.get("params")
        url = f"{host.rstrip('/')}/{endpoint}"
        headers = {"User-Agent": "Git-MCP-Server"}
        if token:
            headers["PRIVATE-TOKEN"] = token
        return http_request(url, method=method, headers=headers, data=params)
    else:
        return {"error": f"Unknown tool: {name}"}

def handle_jsonrpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "git-mcp-server",
                    "version": "1.0.0"
                }
            }
        }
    elif method == "notifications/initialized":
        return None
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": TOOLS
            }
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        result = execute_tool(tool_name, arguments)
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2, ensure_ascii=False)
                    }
                ]
            }
        }
    else:
        if req_id is not None:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            }
        return None

def main():
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            request = json.loads(line)
            response = handle_jsonrpc(request)
            if response is not None:
                sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
                sys.stdout.flush()
        except KeyboardInterrupt:
            break
        except Exception as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32603,
                    "message": str(e)
                }
            }
            sys.stdout.write(json.dumps(err_resp) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
