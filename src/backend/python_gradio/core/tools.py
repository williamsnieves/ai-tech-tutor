import json
from typing import Dict, List, Any, Tuple
import requests
from datetime import datetime, timedelta

def get_terraform_guide(format: str = "text"):
    """Get a comprehensive guide for Terraform setup and usage."""
    guide_steps = [
        {
            "title": "Install Terraform",
            "details": {
                "macOS": "brew tap hashicorp/tap\nbrew install hashicorp/tap/terraform",
                "Ubuntu": (
                    "sudo apt-get update && sudo apt-get install -y gnupg software-properties-common\n"
                    "wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor > hashicorp-archive-keyring.gpg\n"
                    "sudo mv hashicorp-archive-keyring.gpg /usr/share/keyrings/\n"
                    "echo \"deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] "
                    "https://apt.releases.hashicorp.com $(lsb_release -cs) main\" | sudo tee /etc/apt/sources.list.d/hashicorp.list\n"
                    "sudo apt update && sudo apt install terraform"
                ),
                "Verify": "terraform -version"
            }
        },
        {
            "title": "Set Up Project Directory",
            "details": "mkdir terraform-demo && cd terraform-demo\ntouch main.tf"
        },
        {
            "title": "Configure Provider",
            "details": '''provider "aws" {
  region = "us-east-1"
}'''
        },
        {
            "title": "Set AWS Credentials",
            "details": {
                "Option 1 (Env Vars)": (
                    'export AWS_ACCESS_KEY_ID="your-access-key"\n'
                    'export AWS_SECRET_ACCESS_KEY="your-secret-key"'
                ),
                "Option 2 (AWS CLI)": "aws configure"
            }
        },
        {
            "title": "Define Infrastructure Resource (EC2)",
            "details": '''resource "aws_instance" "example" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"
  tags = {
    Name = "TerraformInstance"
  }
}'''
        },
        {
            "title": "Initialize Terraform",
            "details": "terraform init"
        },
        {
            "title": "Plan Infrastructure",
            "details": "terraform plan"
        },
        {
            "title": "Apply Configuration",
            "details": "terraform apply"
        },
        {
            "title": "Destroy Infrastructure",
            "details": "terraform destroy"
        },
        {
            "title": "Typical File Structure",
            "details": '''terraform-demo/
├── main.tf           # main resources
├── variables.tf      # input variables
├── outputs.tf        # output values
├── terraform.tfvars  # values for variables'''
        },
        {
            "title": "Advanced Topics (Optional)",
            "details": [
                "Use modules for reusable blocks",
                "Remote state in S3 (terraform backend)",
                "Workspaces for environments",
                "CI/CD integration"
            ]
        }
    ]

    if format == "steps":
        return guide_steps
    else:
        # Convert steps to readable string
        output = []
        for step in guide_steps:
            output.append(f"🔹 {step['title']}")
            details = step["details"]
            if isinstance(details, dict):
                for k, v in details.items():
                    output.append(f"\n  ▶️ {k}:\n{indent(v)}")
            elif isinstance(details, list):
                for item in details:
                    output.append(f"  - {item}")
            else:
                output.append(indent(details))
            output.append("")  # spacer line
        return "\n".join(output)

def get_github_trending_repos(topic: str, days: int = 7, limit: int = 5) -> str:
    """
    Get trending GitHub repositories for a specific topic.
    
    Args:
        topic (str): The technical topic to search for
        days (int): Number of days to look back for trending repos
        limit (int): Maximum number of repositories to return
        
    Returns:
        str: Formatted string with repository information
    """
    try:
        # Calculate the date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Format dates for GitHub API
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
        
        # GitHub API endpoint
        url = "https://api.github.com/search/repositories"
        params = {
            "q": f"topic:{topic} created:{start_date_str}..{end_date_str}",
            "sort": "stars",
            "order": "desc",
            "per_page": limit
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("items"):
            return f"No trending repositories found for topic '{topic}' in the last {days} days."
        
        # Format the response
        output = [f"🔍 Trending {topic} repositories from the last {days} days:\n"]
        
        for repo in data["items"]:
            stars = repo.get("stargazers_count", 0)
            forks = repo.get("forks_count", 0)
            description = repo.get("description", "No description available")
            language = repo.get("language", "Unknown")
            
            output.append(f"📦 **{repo['name']}**")
            output.append(f"  - Description: {description}")
            output.append(f"  - Language: {language}")
            output.append(f"  - Stars: ⭐ {stars:,}")
            output.append(f"  - Forks: 🔄 {forks:,}")
            output.append(f"  - URL: {repo['html_url']}\n")
        
        return "\n".join(output)
        
    except requests.exceptions.RequestException as e:
        return f"Error fetching GitHub data: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def indent(text, prefix="    "):
    """Helper function to indent text."""
    return "\n".join([prefix + line for line in text.strip().splitlines()])

# Tool definitions for LLM
terraform_function = {
    "name": "get_terraform_guide",
    "description": "Get a comprehensive guide for Terraform setup and usage.",
    "parameters": {
        "type": "object",
        "properties": {
            "format": {
                "type": "string",
                "description": "The format of the guide (text or steps)",
                "enum": ["text", "steps"]
            }
        },
        "required": ["format"],
        "additionalProperties": False
    }
}

github_function = {
    "name": "get_github_trending_repos",
    "description": "Get trending GitHub repositories for a specific technical topic.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The technical topic to search for (e.g., 'python', 'machine-learning', 'docker')"
            },
            "days": {
                "type": "integer",
                "description": "Number of days to look back for trending repos",
                "default": 7
            },
            "limit": {
                "type": "integer",
                "description": "Maximum number of repositories to return",
                "default": 5
            }
        },
        "required": ["topic"],
        "additionalProperties": False
    }
}

# Tool configuration
tools = [
    {"type": "function", "function": terraform_function},
    {"type": "function", "function": github_function},
]

# Map of function names to their implementations
tool_function_map = {
    "get_terraform_guide": get_terraform_guide,
    "get_github_trending_repos": get_github_trending_repos,
}

def handle_tool_calls(tool_calls: List[Any]) -> Tuple[List[Dict[str, Any]], str]:
    """
    Handle tool calls from the LLM.
    
    Args:
        tool_calls: List of tool calls from the LLM
        
    Returns:
        Tuple of (tool_messages, last_result)
    """
    tool_messages = []
    last_result = None

    for tool_call in tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        if function_name not in tool_function_map:
            raise ValueError(f"Unhandled function: {function_name}")

        result = tool_function_map[function_name](**arguments)
        last_result = result

        tool_messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps({**arguments, "result": result}),
        })
    
    return tool_messages, last_result 